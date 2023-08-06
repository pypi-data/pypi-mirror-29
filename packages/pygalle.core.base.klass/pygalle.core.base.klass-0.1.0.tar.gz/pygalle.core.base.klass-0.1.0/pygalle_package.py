#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
---
This file is part of pygalle.core.base.klass
Copyright (c) 2018 SAS 9 Février.
Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
---
"""

import configparser
import os

SETUP_FILENAME = 'setup.cfg'
SECTION_NAME = 'pigalle-package'

configParser = configparser.RawConfigParser()
configFilePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), SETUP_FILENAME)
configParser.read(configFilePath)


CONFIGURATION = dict()
KEYS = ['name', 'version', 'author', 'email', 'copyright', 'credits', 'license', 'maintainer', 'status', 'description']

for key in KEYS: CONFIGURATION[key.lower()] = configParser.get(SECTION_NAME, key)
