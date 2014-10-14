#!/usr/bin/env python
# This file is part of Scarlett.
# Copyright 2014, Behanceops.

import sys
from tests.unit import ScarlettTestCase
from nose.plugins.attrib import attr

class ListenerTestCase(ScarlettTestCase):

    def setUp(self):
        super(ScarlettTestCase, self).setUp()

    @attr(listener=True,pocketsphinx=True,gstreamer=True)
    def test_scarlett_attributes(self):
        pass

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
