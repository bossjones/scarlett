# This file is part of Scarlett.
# Copyright 2014, bossjones.

"""Some common functionality for Scarlett test cases."""

from tests.compat import mock, unittest

import time
import sys
import os
import tempfile

import logging
import scarlett
from scarlett.constants import *


class ScarlettTestCase(unittest.TestCase):

    """A unittest.TestCase subclass that saves and restores Anaconda
    global configuration. This allows tests to make temporary
    modifications that will then be automatically removed when the test
    completes. Hardcoding with mir for the moment till everything works
    """

    connection_class = None

    @classmethod
    def setUpClass(cls):
        super(ScarlettTestCase, cls).setUpClass()
        # ScarlettTestCase you follow Python's logging module's documentation's
        # recommendation about naming your module's logs after the module's
        # __name__,the following getLogger call should fetch the same logger
        # you use in the scarlett module
        scarlett_log = logging.getLogger(scarlett.__name__)
        cls._scarlett_log_handler = MockLoggingHandler(level='DEBUG')
        # scarlett_log.addHandler(cls.scarlett_log_handler)
        scarlett_log.addHandler(MockLoggingHandler())
        cls.scarlett_log_messages = cls._scarlett_log_handler.messages

    def setUp(self):
        super(ScarlettTestCase, self).setUp()
        self._scarlett_log_handler.reset()
        import scarlett
        self.scarlett = scarlett

    # Source: http://stackoverflow.com/questions/899067/how-should-i-verify-a-log-message-when-testing-python-code-under-nose/20553331#20553331
    # TODO: TEST LOG MESSAGES # def test_scarlett_objects_fromble_nicely(self):
    # TODO: TEST LOG MESSAGES #     # Do a bunch of frombling with scarlett objects
    # TODO: TEST LOG MESSAGES #     # Now check that they've logged 5 frombling messages at the INFO level
    # TODO: TEST LOG MESSAGES #     self.assertEqual(len(self.scarlett_log_messages['info']), 5)
    # TODO: TEST LOG MESSAGES #     for info_message in self.scarlett_log_messages['info']:
    # TODO: TEST LOG MESSAGES #         self.assertIn('fromble', info_message)

    def assert_request_parameters(self, params, ignore_params_values=None):
        """Verify the actual parameters sent to the service API."""
        request_params = self.actual_request.params.copy()
        if ignore_params_values is not None:
            for param in ignore_params_values:
                # We still want to check that the ignore_params_values params
                # are in the request parameters, we just don't need to check
                # their value.
                self.assertIn(param, request_params)
                del request_params[param]
        self.assertDictEqual(request_params, params)

    def default_body(self):
        return ''

    def create_service_connection(self, **kwargs):
        if self.connection_class is None:
            raise ValueError("The connection_class class attribute must be "
                             "set to a non-None value.")
        return self.connection_class(**kwargs)

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


class MockScarlettWithConfigTestCase(ScarlettTestCase):

    def setUp(self):
        super(ScarlettTestCase, self).setUp()

    def tearDown(self):
        self.config_patch.stop()
        self.has_config_patch.stop()
        self.environ_patch.stop()

class MockLoggingHandler(logging.Handler):

    """Mock logging handler to check for expected logs."""

    def __init__(self, *args, **kwargs):
        self.reset()
        logging.Handler.__init__(self, *args, **kwargs)

    def emit(self, record):
        self.messages[record.levelname.lower()].append(record.getMessage())

    def reset(self):
        self.messages = {
            'debug': [],
            'info': [],
            'warning': [],
            'error': [],
            'critical': [],
        }
