# -*- coding: utf-8 -*-
#
# Copyright (C) 2012 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals,
# listed below:
#
# Author: Xabier Larrakoetxea <xabier.larrakoetxea@deusto.es>
# Author: Pablo Orduña <pablo.orduna@deusto.es>
# Author: Luis Rodriguez <luis.rodriguezgil@deusto.es>
#
# These authors would like to acknowledge the Spanish Ministry of science
# and innovation, for the support in the project IPT-2011-1558-430000
# "mCloud: http://innovacion.grupogesfor.com/web/mcloud"
#

import os
import uuid
import json
import hashlib
import urllib2
import datetime
import traceback

from functools import wraps

from flask import render_template, request, url_for, flash, redirect, session, abort, Response, render_template_string
from werkzeug import secure_filename

from wcloud.flaskapp import db, app
from wcloud import utils
from wcloud.forms import RegistrationForm, LoginForm, ConfigurationForm, DisabledConfigurationForm, DeployForm
from wcloud.models import User, Token, Entity
from wcloud.tasks.create import deploy_weblab_instance

SESSION_TYPE = 'labdeployer_admin'

opener = urllib2.build_opener(urllib2.ProxyHandler({}))


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/about')
def about():
    return render_template('about.html')


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logged_in = session.get('logged_in', False)
        session_type = session.get('session_type', '')
        if not logged_in or session_type != SESSION_TYPE:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)

    return decorated


@app.route('/')
def index():
    if session.get('logged_in', False):
        return redirect(url_for('home'))

    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        email = form.email.data
        password = form.password.data

        user = User.query.filter_by(email=email).first()

        #User exists?
        if user is None:
            flash("Invalid credentials", "error")
        else:
            #User is active
            if not user.active:
                flash(
                    "Your account isn't active. Follow the e-mail instructions. If you didn't receive it, check the SPAM directory or contact the admin at %s." %
                    app.config['ADMIN_MAIL'], 'error')
                return redirect(url_for('index'))

            #If exists and is active check the password
            hash_password = hashlib.sha1(password).hexdigest()

            if user.password == hash_password:

                #Insert data in session
                session['logged_in'] = True
                session['session_type'] = SESSION_TYPE
                session['user_id'] = user.id
                session['user_email'] = user.email
                session['is_admin'] = user.is_admin

                flash('Logged in', 'success')

                #Redirect
                next_url = request.args.get('next')
                if next_url != '' and next_url != None:
                    return redirect(next_url)

                return redirect(url_for('configure'))
            else:
                flash("Invalid credentials", "error")

    next_url = request.args.get('next')
    return render_template('login.html', form=form, next=next_url)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Endpoint for registering a new user. Depending on the configuration, mail confirmation
    will be required or not.
    """
    form = RegistrationForm(request.form)

    if not app.config['RECAPTCHA_ENABLED']:
        del form.recaptcha

    if request.method == 'POST' and form.validate():
        # Extract data from the form
        full_name = form.full_name.data
        email = form.email.data
        password = form.password.data

        # Create user
        user = User(email, unicode(hashlib.sha1(password).hexdigest()), full_name)
        user.active = False
        user.creation_date = datetime.datetime.now()
        user.ip_address = request.headers.get('HTTP_X_FORWARDED_FOR', request.remote_addr)

        mail_confirmation = app.config["MAIL_CONFIRMATION_ENABLED"]

        # Add to database
        token = Token(str(uuid.uuid4()), datetime.datetime.now())
        user.token = token

        if not mail_confirmation:
            user.active = True

        db.session.add(user)
        db.session.commit()

        try:
            from_email = 'weblab@deusto.es'

            body_html = """ <html>
                                <head></head>
                                <body>
                                  <p>New registered user in wCloud: %s</p>
                                </body>
                              </html>""" % email
            body = "New registered user: %s" % email
            subject = 'New registration'

            utils.send_email(app, body, subject, from_email, app.config['ADMINISTRATORS'], body_html)
        except:
            traceback.print_exc()

        if mail_confirmation:
            # Create email
            from_email = 'weblab@deusto.es'

            link = url_for('confirm', email=email, token=token.token, _external=True)
            body_html = """ <html>
                                <head></head>
                                <body>
                                  <p>Welcome!<p>
                                  <p>This is the wcloud system, which creates new WebLab-Deusto instances.
                                  Your account is ready, and you can activate it:</p>
                                  <ul>
                                    <li><a href="%(link)s">%(link)s</a>.</li>
                                  </ul>
                                  <p>If you didn't register, feel free to ignore this e-mail.</p>
                                  <p>Best regards,</p>
                                  <p>WebLab-Deusto team</p>
                                </body>
                              </html>""" % dict(link=link)
            print(body_html)
            body = """Welcome to wcloud. Click %s to confirm your registration.""" % link
            subject = 'wCloud registration'


            # Send email
            try:
                utils.send_email(app, body, subject, from_email, user.email, body_html)
            except:
                db.session.delete(token)
                db.session.delete(user)
                db.session.commit()
                flash(
                    "There was an error sending the e-mail. This might be because of a invalid e-mail address. Please re-check it.",
                    "error")
                return render_template('register.html', form=form)
            else:
                flash("Mail sent to %s from %s with subject '%s'. Check your SPAM folder if you don't receive it." % (
                    user.email, from_email, subject), 'success')

            flash("""Thanks for registering. You have an
                  email with the steps to confirm your account""", 'success')

        # No mail confirmation.
        else:
            flash("""Thanks for registering. Your account is ready. Please, login.""", 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


@app.route('/confirm')
def confirm(email=None, token=None):
    if email is None:
        email = request.args.get('email')
    if token is None:
        token = request.args.get('token')

    if not email or not token:
        if not email:
            flash("Error: 'email' field misssing", 'error')
        if not token:
            flash("Error: 'token' field misssing", 'error')
        return render_template('errors.html', message="Fields missing")

    user = User.query.filter_by(email=email).first()

    #User exists?
    if user is None:
        flash('Register first please', 'error')
        return redirect(url_for('register'))
        #Check token
    if user.token.token != token:
        flash('Confirmation failed', 'error')
        return redirect(url_for('login'))

    #verify account
    user.active = True

    #update in database the active flag
    db.session.add(user)
    db.session.commit()

    flash('Account confirmed. Please login', 'success')
    return redirect(url_for('login'))


@app.route('/dashboard/home')
@login_required
def home():
    email = session['user_email']
    user = User.query.filter_by(email=email).first()
    if user is None:
        return redirect(url_for('logout'))
    return render_template('home.html', user=user)


@app.route('/dashboard/configure', methods=['GET', 'POST'])
@login_required
def configure():
    email = session['user_email']
    user = User.query.filter_by(email=email).first()

    if user is None:
        flash("User not found")
        return redirect(url_for('logout'))

    if user.entity is not None and user.entity.deployed:
        enabled = False
        form = DisabledConfigurationForm(request.form)
    else:
        enabled = True
        form = ConfigurationForm(request.form)

    if user.entity is not None and user.entity.logo is not None:
        logo_available = True
    else:
        logo_available = False

    if request.method == 'POST' and form.validate():
        if not enabled:
            flash("You can not change the entity once deployed.")
            return render_template('configuration.html', form=form, enabled=enabled, logo_available=logo_available)

        # Exract data from the form
        logo = request.files['logo']
        logo_data = logo.stream.read()
        logo_ext = (logo.name or u'').split('.')[-1]
        if len(logo_ext) not in (3, 4):
            # That's not an extension
            logo_ext = u'jpeg'
        name = form.name.data
        base_url = form.base_url.data
        link_url = form.link_url.data
        google_analytics_number = form.google_analytics_number.data

        logo_available = True

        # Create entity
        if user.entity is None:
            entity = Entity(name, base_url)
            entity.logo = logo_data
            entity.logo_ext = logo_ext
            entity.link_url = link_url
            entity.google_analytics_number = google_analytics_number
            user.entity = entity

        # Update
        else:
            if logo_data is not None and logo_data != '':
                user.entity.logo = logo_data
                user.entity.logo_ext = logo_ext
            if name is not None: user.entity.name = name
            if base_url is not None: user.entity.base_url = base_url
            if link_url is not None: user.entity.link_url = link_url
            if google_analytics_number is not None:
                user.entity.google_analytics_number = google_analytics_number

        # Save
        db.session.add(user)
        db.session.commit()

        flash('Configuration saved.', 'success')

        if request.form.get('action', '') == 'savedeploy':
            return redirect(url_for('deploy'))

    else:
    # Get user
        email = session['user_email']
        user = User.query.filter_by(email=email).first()
        if user is None:
            return redirect(url_for('logout'))
        entity = user.entity
        if entity is not None:
            form.name.data = entity.name
            form.base_url.data = entity.base_url
            form.link_url.data = entity.link_url
            form.google_analytics_number.data = entity.google_analytics_number
    return render_template('configuration.html', form=form, enabled=enabled, logo_available=logo_available)


@app.route('/dashboard/logo')
@login_required
def logo():
    email = session['user_email']
    user = User.query.filter_by(email=email).first()
    entity = user.entity
    if entity is None or entity.logo is None:
        return abort(404)
    return Response(entity.logo, headers={'Content-Type': 'image/%s' % entity.logo_ext})


@app.route('/dashboard/undeploy', methods=["GET", "POST"])
@login_required
def undeploy():

    if not (app.config["DEBUG"] and app.config["DEBUG_UNDEPLOY_ENABLED"]):
        return "Not allowed with the current configuration", 405

    email = session['user_email']
    user = User.query.filter_by(email=email).first()
    entity = user.entity

    if request.method == "GET":

        return render_template_string(
            """
            <p>
            Are you sure you want to undeploy?
            </p>

            <form name="input" method="post">
                <input type="submit" value="Undeploy"/>
            </form>
            """
            )

    else:

        entity.deployed = False
        db.session.add(entity)
        db.session.commit()

        return render_template_string(
            """
            <p>
            Undeployed.
            </p>

            <a href="{{ url_for("login") }}">Back</a>

            """
        )


@app.route('/dashboard/deploy', methods=['GET', 'POST'])
@login_required
def deploy():
    form = DeployForm(request.form)

    # Get user settings
    email = session['user_email']
    user = User.query.filter_by(email=email).first()
    entity = user.entity

    enabled = not user.entity.deployed

    base_url = app.config['PUBLIC_URL']

    if request.method == 'GET':
        # If it was not filled
        if not form.admin_name.data:
            form.admin_name.data = user.full_name
            form.admin_user.data = 'admin'
            form.admin_email.data = user.email

    if request.method == 'POST' and form.validate():
        if not enabled:
            flash("You have already deployed your system, so you can not redeploy it")
            return render_template('deploy.html', form=form, enabled=enabled)

        admin_user = form.admin_user.data
        admin_name = form.admin_name.data
        admin_email = form.admin_email.data
        admin_password = form.admin_password.data

        if entity is None:
            flash('Configure before using the deployment app', 'error')
            return redirect(url_for('configure'))

        entity.deployed = True
        db.session.add(entity)
        db.session.commit()

        # Deploy

        directory = os.path.join(app.config['DIR_BASE'], entity.base_url)

        result = deploy_weblab_instance.delay(directory, email, admin_user, admin_name, admin_email, admin_password, base_url)
        return redirect(url_for('result', deploy_id=result.task_id))

    return render_template('deploy.html', form=form, enabled=enabled, url=base_url + '/w/' + entity.base_url)

def _report_failure_to_admin(deploy_id, report):

    email = session['user_email']
    from_email = 'weblab@deusto.es'

    link = url_for('result', deploy_id = deploy_id, _external=True)
    body_html = """ <html>
                        <head></head>
                        <body>
                          <p>Error ocurred for deployment (%(deploy_id)s) for user %(email)s<p>
                          <pre>%(report)s</pre>
                          <p>Check it in:</p>
                          <ul>
                            <li>%(link)s</li>
                          </ul>
                          <p>Best regards,</p>
                          <p>wCloud system</p>
                        </body>
                      </html>""" % dict(link=link, deploy_id = deploy_id, email = email, report = report)
    print(body_html)
    body = """Error ocurred in wCloud."""
    subject = 'wCloud failure'

    utils.send_email(app, body, subject, from_email, app.config['ADMINISTRATORS'], body_html)

@app.route('/dashboard/deploy/result/<deploy_id>')
@login_required
def result(deploy_id):
    result = deploy_weblab_instance.AsyncResult(deploy_id)
    if isinstance(result.result, dict):
        email = result.result.get('email')
        if email is not None and email != session['user_email'] and not session['is_admin']:
            return "You don't have permissions to see this deployment id"
        # If email is None or it's not a dict, it's pending or something like that.

    loop = True
    if result.status == 'SUCCESS':
        return redirect(url_for('result_ready', deploy_id=deploy_id))

    if result.result is None:
        output = 'Pending job...'
    else:
        if isinstance(result.result, dict):
            if result.result.get('is_error'):
                loop = False
                flash("Deployment failed. Contact the administrators at <a href='mailto:weblab@deusto.es'>weblab@deusto.es</a>.", "error")
                _report_failure_to_admin(deploy_id, result.result['report'])
                print result.result['report']
            output = result.result.get('output', 'No output yet')
        else:
            loop = False
            print result.result
            output = "Invalid result. Contact administrator."

    return render_template('result.html',
                           status=result.status,
                           stdout=output,
                           deploy_id=deploy_id, loop=loop)


@app.route('/dashboard/deploy/ready/<deploy_id>')
@login_required
def result_ready(deploy_id):
    result = deploy_weblab_instance.AsyncResult(deploy_id)
    if isinstance(result.result, dict):
        email = result.result.get('email')
        if email is not None and email != session['user_email'] and not session['is_admin']:
            return "You don't have permissions to see this deployment id"
        # If email is None or it's not a dict, it's pending or something like that.

    if result.status != 'SUCCESS':
        return redirect(url_for('result', deploy_id=deploy_id))

    url = 'not provided'
    if result.result is None:
        output = 'Pending job...'
    else:
        if isinstance(result.result, dict):
            if result.result.get('is_error'):
                _report_failure_to_admin(deploy_id, result.result['report'])
                flash("Deployment failed. Contact the administrators at <a href='mailto:weblab@deusto.es'>weblab@deusto.es</a>.", "error")

            output = result.result.get('output', 'No output yet')
            url = result.result.get('url', 'No URL provided')
            print result.result['report']
        else:
            output = "Invalid result. Contact admin"
            url = "Invalid result. Contact admin"

    return render_template('result-ready.html',
                           status=result.status,
                           stdout=output,
                           deploy_id=deploy_id, url=url)


@app.route('/logout')
@login_required
def logout():
    #Insert data in session    
    session.pop('logged_in', None)
    session.pop('session_type', None)
    session.pop('user_id', None)
    session.pop('user_email', None)
    session.pop('is_admin', None)

    flash('Logged out', 'success')
    return redirect(url_for('index'))
