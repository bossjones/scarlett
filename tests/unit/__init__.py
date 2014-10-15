#!/usr/bin/env python
# This file is part of Scarlett.
# Copyright 2014, Behanceops.

"""Some common functionality for Scarlett test cases."""

# Use unittest2 on Python < 2.7.
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import scarlett
import os

class ScarlettTestCase(unittest.TestCase):

    """A unittest.TestCase subclass that saves and restores Anaconda
    global configuration. This allows tests to make temporary
    modifications that will then be automatically removed when the test
    completes. Hardcoding with mir for the moment till everything works
    """

    def setUp(self):
        pass

    """
    For the moment this isn't the best tearDown function,
    but we should keep it to remind ourselves to add more to it
    in the future
    """

    def tearDown(self):
        pass

    def assertExists(self, path):
        self.assertTrue(os.path.exists(path),
                        'file does not exist: %s' % path)

    def assertNotExists(self, path):
        self.assertFalse(os.path.exists(path),
                         'file exists: %s' % path)
