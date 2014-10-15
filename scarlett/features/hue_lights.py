#!/usr/bin/env python

import scarlett
from features import Feature
#from phue import Bridge

class FeatureHueLights(Feature):

    capability = []

    def __init__(self, host, config, provider):

        Feature.__init__(self, "hue")
        if self.module_exists("phue"):
          from phue import Bridge
          self.b = Bridge(scarlett.config.get('hue', 'bridge'))
          self.b.connect()

    def add_auth(self, http_request):
        pass

    def light_play(self,cmd):
        subprocess.call([cmd],shell=True)
        self.keyword_identified = 0
        self.voice.play('pi-response')
