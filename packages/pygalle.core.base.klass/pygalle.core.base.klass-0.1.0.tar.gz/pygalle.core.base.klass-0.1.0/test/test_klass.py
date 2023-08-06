#!/usr/bin/env python

# -*- coding: utf-8 -*-

""" This file is part of pygalle.core.base.klass

    Copyright (c) 2018 SAS 9 Février.

    Distributed under the MIT License (license terms are at http://opensource.org/licenses/MIT).
"""

import unittest
import inspect

from pygalle.core.base.klass import PygalleBaseClass


class KlassBaseTest(unittest.TestCase):
    """ Unit tests for PygalleBaseClassTest.
    """

    def test_isclass(self):
        """ Is {PygalleBaseClass} really a class ? """
        self.assertEqual(inspect.isclass(PygalleBaseClass), True)

    def test_create_instance(self):
        """ Create a new instance of {PygalleBaseClass} """
        self.assertIsInstance(PygalleBaseClass(), PygalleBaseClass)

def main():
    """ Entry point.
    """
    unittest.main()

if __name__ == '__main__':
    main()

