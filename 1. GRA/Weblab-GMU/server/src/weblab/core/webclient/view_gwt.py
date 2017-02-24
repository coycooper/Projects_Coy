#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
#
# Copyright (C) 2005 onwards University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals,
# listed below:
#
# Author: Pablo Orduña <pablo@ordunya.com>
#         Luis Rodriguez <luis.rodriguez@opendeusto.es>
#
from __future__ import print_function, unicode_literals

import traceback
import requests
from flask import send_from_directory, render_template, request, url_for

from weblab.core.wl import weblab_api
from weblab.util import data_filename
from weblab.core.webclient import login_required

def _process_index():
    config_path = request.args.get('c')
    client_config = {
        'config': {},
        'client_code_name': "",
        'base_location': url_for('json.service_url').rsplit('json/', 0)[0],
        'mobile': False,
        'facebook': False,
        'start_reserved': False
    }

    if config_path and config_path.count('/') > 3 and '://' in config_path:
        # Extract the experiment name and the category name
        base_url, category_name, experiment_name, config_js = config_path.rsplit('/', 3)
        category_name = requests.utils.unquote(category_name)
        experiment_name = requests.utils.unquote(experiment_name)

        # Check that it's us who has generated this
        original_url = requests.utils.unquote(url_for('core_webclient.lab_config', experiment_name = experiment_name, category_name = category_name, _external = True))
        if original_url.split('://', 1)[1] == config_path.split('://', 1)[1]:
            # It's a valid URL
            experiment_config = {}
            client_name = ''
            try:
                experiment = weblab_api.db.get_experiment(experiment_name, category_name)
            except Exception as ex:
                traceback.print_exc()
                experiment = None

            if experiment is not None:
                client_config['config'] = experiment.client.configuration
                client_config['client_code_name'] = experiment.client.client_id

    return render_template('webclient/gwt-index.html', client_config=client_config)

@weblab_api.route_webclient('/gwt/')
def gwt_index():
    return _process_index()

@weblab_api.route_webclient('/gwt/<path:path>')
def gwt(path = ''):
    # If it's the index, generate something
    if path in ('', 'index.html', 'index.htm'):
        return _process_index()
    
    # Otherwise, just
    base_directory = data_filename('war')
    return send_from_directory(base_directory, path)

