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
# Author: Pablo Orduña <pablo@ordunya.com>
#         Luis Rodriguez-Gil <luis.rodriguezgil@deusto.es>
#
from __future__ import print_function, unicode_literals


def getBoardTypesList():
    """
    Retrieves the list of possible Board types. The Board type is passed to the Programmer, and its activity
    may depend on it.
    :return:
    """
    return ('PLD', 'FPGA')
