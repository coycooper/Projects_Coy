#!/usr/bin/env python
# -*-*- encoding: utf-8 -*-*-
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
# Author: Luis Rodriguez Gil <luis.rodriguezgil@deusto.es>
#
import base64
import json
import time
import traceback
import array
import threading
import requests

from flask import make_response, request, jsonify
import redis

from weblab.core.wl import weblab_api

# # PROTOCOL
#
# ## ACTION: Create a new job
# METHOD: POST to /compiserv/queue/armc
# PARAMETERS: Can receive the file as a multipart file, or as raw data.
#
# RETURNS:
# A JSON object:
# { result: <result>, // <result> is 'accepted' or 'denied'
#   uid: <uid>, // only if result is 'accepted'
# }
#
#
# ## ACTION: Check the state of a job
# METHOD: GET to /compiserv/queue/<uid>
# PARAMETERS: The <uid>
#
# RETURNS:
# A JSON object:
# { state: <state>, // <state> is 'finished' if the task is done or failed, 'unfinished' if it is reportedly in progress or
#                      in queue, and 'not_found' if it could not be found.
#
# }
#
#
# Note: The BinaryFile and LogFile are returned from the remote compilation service in array-of-byte-integers format.
#

BASE_URL = "http://llcompilerservice.azurewebsites.net/CompilerGeneratorService.svc"
POST_URL = BASE_URL + "/PutCompilerTask/uvision"
GET_URL = BASE_URL + "/GetCompilerTask/{0}/{1}"

# Connect forever to the redis server
_redis = redis.Redis("localhost")
""" type : redis.Redis """


@weblab_api.route_web('/compiserv/')
def compiserve():
    msg = "Welcome to the Compiler Service. This is not yet implemented."
    data = {"msg": msg}
    contents = json.dumps(data, indent=4)
    response = make_response(contents)
    response.content_type = 'application/json'
    return response


@weblab_api.route_web('/compiserv/queue/armc', methods=["POST"])
def compiserve_queue_armc_post():
    """
    Enqueues an ARMC synthesization job. This can be done by any client.
    :return:
    """

    response = {
        "result": ""  # accepted or denied
    }

    file_contents = None

    if request.data is not None:
        file_contents = request.data
    elif request.files is not None and len(request.files) > 0:
        file_contents = request.files['file']
        # TO-DO

    if file_contents is None:
        response['result'] = 'denied'
        response['reason'] = 'no_file_sent'

    else:
        # Send to AZURE SERVICE
        resp = requests.post(POST_URL, files={"main.c": ("main.c", file_contents, "text/plain")})
        json_resp = resp.json()
        generated_date = json_resp["GeneratedDate"]
        id = json_resp["ID"]
        token = json_resp["TokenID"]

        response['result'] = 'accepted'
        uid = "{0}+{1}".format(id, token)
        response['uid'] = uid

        job_key = "compiserv::jobs::{0}".format(uid)

        # Store the JOB.
        _redis.hset(job_key, "state", "queued")

        print("JOB PUT IN QUEUE: Thread: {0}".format(threading.current_thread()))

    contents = json.dumps(response, indent=4)
    response = make_response(contents)
    response.content_type = 'application/json'
    return response


@weblab_api.route_web('/compiserv/queue/armc/<uid>', methods=["GET"])
def compiserve_queue_get(uid):
    """
    Enquiries about the status of a specific job. This can be done by any client.
    :return:
    """

    try:

        print("Received UID is: " + uid)

        job_key = "compiserv::jobs::{0}".format(uid)

        result = {
            "state": ""
        }

        if not _redis.exists(job_key):
            return jsonify(state='not_found')

        # Split the UID into its components.
        id, tokenid = uid.split("+", 1)

        # Retrieve the state of the remote JOB
        resp = requests.get(GET_URL.format(id, tokenid))
        jsresp = resp.json()

        # BinaryFile, CompletedDate, LogFile, State
        state = jsresp['State'].lower()

        if state == 'finished':

            # The job is not active anymore, but it may have succeeded or failed.

            print "[DEBUG]: CompiServ finished with {0}. From thread: {1}".format(uid, threading.current_thread())

            binary_file = jsresp['BinaryFile']  # type: list[int]
            completed_date = jsresp['CompletedDate']
            log_file = jsresp['LogFile']
            compile_result = 'success' if binary_file is not None else 'error'

            # Store the binary file as a byte array.
            # TODO: Check whether flask supports bytearray

            # This converts from an array of integers representing the bytes, to a bytes str (or in
            # Python 3, to a 'bytes'.
            binary_file = array.array('B', binary_file).tostring()
            binary_file = array.array('B', str(binary_file)).tostring()
            log_file = array.array('B', str(log_file)).tostring()

            # Store the files in the redis-powered job
            _redis.hset(job_key, "binary_file", binary_file)
            _redis.hset(job_key, "completed_date", completed_date)
            _redis.hset(job_key, "log_file", log_file)
            _redis.hset(job_key, "result", compile_result)

            if compile_result == 'error':
                result['state'] = 'failed'
            else:
                result['state'] = 'done'

            print("[DEBUG] Compiserv result saved.")

        elif state.startswith('unfinished'):
            splits = state.split(":")
            number = int(splits[1].strip())
            result['state'] = 'queued'
            result['position'] = number

        else:
            raise Exception("Unrecognized job state: " + state)

        contents = json.dumps(result, indent=4)
        response = make_response(contents)
        response.content_type = 'application/json'
        return response

    except Exception as ex:
        tb = traceback.format_exc()
        return jsonify(state='error', traceback=tb)


@weblab_api.route_web('/compiserv/result/<uid>/outputfile', methods=["GET"])
def compiserve_result_outputfile(uid):
    """
    Requests the result (outputfile) of a job. This is only to be called INTERNALLY by the Experiment Servers
    and is protected by a token.
    :return:
    """

    try:

        # TODO: Clean this.
        # This is just an attempt of bug work-around. It would be better to properly fix this.
        if "+" not in uid:
            uid = uid.replace(" ", "+")

        job_key = "compiserv::jobs::{0}".format(uid)

        if not _redis.exists(job_key):
            result = {
                'result': 'error',
                'msg': "Job not found. Searched for: {0}".format(uid)
            }
            result = json.dumps(result, indent=4)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json"
            return response

        job_result = _redis.hget(job_key, "result")

        # Find the file in redis
        # It should return a binary str (which is what was stored).
        binary_file = _redis.hget(job_key, "binary_file")  # type: str

        if binary_file is not None and job_result == "success":
            file_contents = binary_file
            response = make_response(file_contents)
            response.headers["Content-Disposition"] = "attachment; filename=result.bin"
            response.headers["Content-Type"] = "application/octet-stream"
        else:  #
            log_file = _redis.hget(job_key, "log_file")
            if log_file is not None:
                log_file = base64.b64encode(log_file)
            result = {
                'result': 'error',
                'msg': 'result not found',
                'log_file': log_file
            }
            result = json.dumps(result, indent=4)
            response = make_response(result)
            response.headers["Content-Type"] = "application/json"

        return response

    except Exception as ex:
        tb = traceback.format_exc()
        return jsonify(state='error', traceback=tb)


@weblab_api.route_web('/compiserv/result/<uid>/logfile', methods=["GET"])
def compiserve_result_logfile(uid):
    """
    Requests the result (logfile) of a job. This is only to be called INTERNALLY by the Experiment Servers
    and is protected by a token.
    :param uid:
    :return:
    """

    # TODO: Clean this.
    # This is just an attempt of bug work-around. It would be better to properly fix this.
    if "+" not in uid:
        uid = uid.replace(" ", "+")

    job_key = "compiserv::jobs::{0}".format(uid)

    if not _redis.exists(job_key):
        result = {
            'result': 'error',
            'msg': "Job not found. Searched for: {0}".format(uid)
        }
        result = json.dumps(result, indent=4)
        response = make_response(result)
        response.headers["Content-Type"] = "application/json"
        return response

    # Find the job log_file in redis.
    log_file = _redis.hget(job_key, "log_file")

    if log_file is not None:
        # TODO: Check the state of the job. Do not assume it is finished.
        file_contents = log_file
        response = make_response(file_contents)
        response.headers["Content-Disposition"] = "attachment; filename=logfile.bin"
        response.headers["Content-Type"] = "application/octet-stream"
    else:  #
        result = {
            'result': 'error',
            'msg': 'result not found'
        }
        result = json.dumps(result, indent=4)
        response = make_response(result)
        response.headers["Content-Type"] = "application/json"

    return response


if __name__ == "__main__":
    print("Testing external service")

    import requests

    program = """
    #include <stdio.h>

    int main()
    {
    }
    """

    resp = requests.post(
        "http://llcompilerservice.azurewebsites.net/CompilerGeneratorService.svc/PutCompilerTask/uvision",
        files={"main.c": ("main.c", program, "text/plain")})
    resp = resp.json()

    id = resp["ID"]
    tid = resp["TokenID"]

    time.sleep(10)
    resp = requests.get(
        "http://llcompilerservice.azurewebsites.net/CompilerGeneratorService.svc/GetCompilerTask/{0}/{1}".format(id,
                                                                                                                 tid))
    print "Req to: " + "http://llcompilerservice.azurewebsites.net/CompilerGeneratorService.svc/GetCompilerTask/{0}/{1}".format(
        id, tid)
    data = resp.content
    print len(data)
    print data
