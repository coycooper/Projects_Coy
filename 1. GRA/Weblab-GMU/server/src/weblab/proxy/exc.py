#!/usr/bin/python
# -*- coding: utf-8 -*-
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
# Author: Jaime Irurzun <jaime.irurzun@gmail.com>
#
from __future__ import print_function, unicode_literals

import weblab.exc as wlExc

class ProxyError(wlExc.WebLabError):
    def __init__(self, *args, **kargs):
        wlExc.WebLabError.__init__(self, *args, **kargs)

#
# from ProxyError
#

class NotASessionTypeError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)

class InvalidReservationIdError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)

class AccessDisabledError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)

class InvalidDefaultTranslatorNameError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)

class FailedToSendCommandError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)

class FailedToSendFileError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)

class NoCurrentReservationError(ProxyError):
    def __init__(self, *args, **kargs):
        ProxyError.__init__(self, *args, **kargs)
