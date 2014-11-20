# This file is part of Scarlett.
# Copyright 2014, Behanceops.

import scarlett
import sys
from tests.unit import unittest, ScarlettTestCase
from nose.plugins.attrib import attr
from scarlett.features.hue_lights import FeatureHueLights


class HueTestCase(ScarlettTestCase):

    def setUp(self):
        super(HueTestCase, self).setUp()

    @attr(hue=True)
    def test_hue_lights(self):
        pass
        #self.hue_test = self.scarlett.connect_hue()
        # self.assertEqual(self.voice_test,Voice())


def suite():
    return unittest.TestLoader().loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
