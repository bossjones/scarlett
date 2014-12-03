# This file is part of Scarlett.
# Copyright 2014, Behanceops.

import scarlett
import sys
import time
import datetime
from tests.unit import unittest, ScarlettTestCase
from nose.plugins.attrib import attr
from scarlett.basics.voice import Voice
from scarlett.brain import ScarlettBrain
from scarlett.features.time import FeatureTime
from nose.plugins.attrib import attr
import mock
from mock import patch
from mock import mock_open

class TimeTestCase(ScarlettTestCase):

    def setUp(self):
        super(TimeTestCase, self).setUp()
        self.now = mock.patch('scarlett.features.time.now', datetime.datetime(2014, 12, 2, 20, 47, 19, 715394))
        self.brain_test = self.scarlett.connect_brain()
        self.voice_test = self.scarlett.connect_voice(self.brain_test)
        self.time_test  = FeatureTime(self.voice_test, self.brain_test)

    @attr(voice=True)
    def test_time(self):
        #self.set_now   =datetime.datetime(2014, 12, 2, 20, 47, 19, 715394)
        # self.assertEqual(self.voice_test,Voice())
        self.assertTrue(self.time_test.get_current_time(),"It is now, 08:47 PM")
        self.assertTrue(self.time_test.get_current_date(),"Today's date is, Tuesday, December 02, 2014")

# from scarlett.features.time import FeatureTime
#                 self.get_time = FeatureTime(self.voice, self.brain)
#                 return self.get_time.time_play()

def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

def voice_play(self,text):
    return "%s" % (text)

def now_test(self):
    return datetime.datetime.now()

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
