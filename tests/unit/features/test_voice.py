# This file is part of Scarlett.
# Copyright 2014, Behanceops.

import scarlett
import sys
from tests.unit import unittest,ScarlettTestCase
from nose.plugins.attrib import attr
from scarlett.basics.voice import Voice

class VoiceTestCase(ScarlettTestCase):

    def setUp(self):
        super(VoiceTestCase, self).setUp()

    @attr(voice=True)
    def test_voice(self):
        self.voice_test = self.scarlett.connect_voice()
        #self.assertEqual(self.voice_test,Voice())

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
