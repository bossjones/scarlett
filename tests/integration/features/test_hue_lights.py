# # This file is part of Scarlett.
# # Copyright 2014, Behanceops.

# import scarlett
# import sys
# from tests.integration import unittest, ScarlettIntegrationTestCase
# from nose.plugins.attrib import attr
# from scarlett.basics.voice import Voice
# from scarlett.brain import ScarlettBrain
# from scarlett.features.hue_lights import FeatureHueLights
# import mock
# from mock import patch
# from mock import mock_open

# class HueIntegrationTestCase(ScarlettIntegrationTestCase):

#     def setUp(self):
#         super(HueIntegrationTestCase, self).setUp()
#         #self.now = mock.patch('scarlett.features.time.now', datetime.datetime(2014, 12, 2, 20, 47, 19, 715394))
#         self.brain_test = self.scarlett.connect_brain()
#         self.voice_test = self.scarlett.connect_voice(self.brain_test)
#         self.hue_test  = FeatureHueLights(self.voice_test, self.brain_test)

#     @attr(hue=True)
#     def test_hue_lights(self):
#         pass
#         #self.hue_test = self.scarlett.connect_hue()
#         # self.assertEqual(self.voice_test,Voice())
#         #self.assertTrue(self.time_test.get_current_time(),"It is now, 08:47 PM")
#         #self.assertTrue(self.time_test.get_current_date(),"Today's date is, Tuesday, December 02, 2014")


# def suite():
#     return unittest.TestLoader().loadTestsFromName(__name__)

# if __name__ == '__main__':
#     unittest.main(defaultTest='suite')
