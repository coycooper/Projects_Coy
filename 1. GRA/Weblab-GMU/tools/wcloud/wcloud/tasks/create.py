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

import sys
from wcloud.actions import wcloud_actions
from wcloud.actions.wcloud_actions import WebLabEnvironmentCreationError
from wcloud.tasks.celery_app import celery_app

import shutil
import traceback
import cStringIO as StringIO

from weblab.admin.script import Creation

def _store_progress(task, result, output, step, report):
    result['output'] = output.getvalue()
    result['step'] = step
    result['report'] = report.getvalue()
    if not task.request.called_directly:
        task.update_state(state='PROGRESS', meta=result)

class TransactionException(Exception):
    pass

class TransactionProcessor(object):
    def __init__(self, task, result, output, report):
        self.rollback_functions = []
        self.task = task 
        self.result = result
        self.output = output
        self.report = report
        self.message = ""
        self.step = 0
 
    def register_rollback(self, rollback_func, *args, **kwargs):
        self.rollback_functions.append((rollback_func, args, kwargs))
 
    def __call__(self, message):
        self.message = message
        return self
 
    def __enter__(self):
        self.output.write(self.message + "... ")
        print(self.message + "... ")
        _store_progress(self.task, self.result, self.output, self.step, self.report)
        return self
 
    def __exit__(self, error_type, error_instance, tb):
        if error_instance is not None:
            error_message = "Error while %s" % self.message
            print("[error]\n")
            self.output.write("[error]\n")
            self.output.write("\n")
            self.output.write(error_message)
            self.output.write("\n")

            self.report.write(self.output.getvalue())
            self.report.write("*" * 40)
            self.report.write("\n\n\n")

            if error_type == WebLabEnvironmentCreationError:
                self.report.write(error_instance.args[1])
                self.report.write("\n")

            traceback.print_exception(error_type, error_instance, tb)
            traceback.print_exception(error_type, error_instance, tb, file = self.report)
            for func, args, kwargs in self.rollback_functions[::-1]:
                self.report.write("Applying rollback %s..." % func.__name__)
                try:
                    func(*args, **kwargs)
                except:
                    self.report.write("[error]\n")
                    traceback.print_exc()
                    traceback.print_exc(file = self.report)
                else:
                    self.report.write("[done]\n")
            
            raise TransactionException(error_message)
        else: 
            print("[done]\n")
            self.output.write("[done]\n")
            _store_progress(self.task, self.result, self.output, self.step, self.report)
        self.step += 1

@celery_app.task(bind=True, name = 'deploy_weblab_instance')
def deploy_weblab_instance(self, directory, email, admin_user, admin_name, admin_email, admin_password, base_url):
    """
    Deploys a new WebLab instance with the specified parameters.

    :param self: Reference to the Task itself, provided by Celery automatically.
    :param directory: The directory (file system) on which the WebLab-Deusto instance will be created.
    :param email: wCloud login of the user creating this instance.
    :param admin_user: generated WebLab-Deusto instance admin login.
    :param admin_name: generated WebLab-Deusto instance admin full name.
    :param admin_email: generated WebLab-Deusto instance admin e-mail.
    :param admin_password: generated WebLab-Deusto instance admin password.
    :param base_url: Relative URL of the system (e.g., /w/deusto/ or whatever).
    :return:
    """
    output = StringIO.StringIO()
    report = StringIO.StringIO()
    result = {'output' : output.getvalue(), 'step' : 0, 'email' : email, 'report' : report.getvalue(), 'is_error' : False, 'error_message' : None }
    transaction = TransactionProcessor(self, result, output, report)

    try:
        ######################################
        #
        # 1. Prepare the system
        #
        transaction.register_rollback(wcloud_actions.rollback_prepare_system, email)

        with transaction("preparing requirements"):
            current_instance_settings = wcloud_actions.prepare_system(email, admin_user, admin_name, admin_password, admin_email)

        #########################################################
        #
        # 2. Create the full WebLab-Deusto environment
        #
        transaction.register_rollback(wcloud_actions.rollback_create_weblab_environment, directory)

        with transaction("creating deployment directory"):
            creation_results = wcloud_actions.create_weblab_environment(directory, current_instance_settings)

        ##########################################################
        #
        # 3. Configure the web server
        #
        transaction.register_rollback(wcloud_actions.rollback_configure_web_server, creation_results)

        with transaction("configuring web server"):
            wcloud_actions.configure_web_server(creation_results)

        ##########################################################
        #
        # 4. Register and start the new WebLab-Deusto instance
        #
        transaction.register_rollback(wcloud_actions.rollback_register_and_start_instance, directory)

        with transaction("registering and starting instance"):
            wcloud_actions.register_and_start_instance(email, directory)

        ##########################################################
        #
        # 5. Check the deployment
        #
        transaction.register_rollback(wcloud_actions.rollback_finish_deployment, email)

        with transaction("checking deployment"):
            wcloud_actions.finish_deployment(email, creation_results["start_port"], creation_results["end_port"])
        
        ##########################################################
        #
        # 6. Service deployed. Configure the response
        #
    except TransactionException as e:
        result['is_error'] = True
        result['error_message'] = e.args[0]
        result['output'] = output.getvalue()
        result['report'] = report.getvalue()
        return result

    output.write("\nCongratulations, your system is ready!")
    result['output'] = output.getvalue()
    result['report'] = report.getvalue()
    result['url'] = base_url + current_instance_settings[Creation.BASE_URL]
    return result

