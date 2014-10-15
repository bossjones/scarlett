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
          self.lights = self.b.lights

    def find_active_lights(self):
        pass

    def find_light(self,light_name):
        return self.b.get_light(light_name)

    def brighten_light(self,light_name):
        command =  {'bri' : 240}
        return self.b.set_light(light_name, command)

    def turn_on_all_lights(self):
        lights_list = self.b.get_light_objects('list')
        for light in lights_list:
            light.on = True
            light.colortemp = 400
            light.bri = 127

    def brighten_lights_all(self,light_name):
        command =  {'bri' : 240}
        return self.b.set_light(light_name, command)

    def darken_light(self,light_name):
        command =  {'bri' : 100}
        return self.b.set_light(light_name, command)

    def print_light_names(self):
        for l in self.lights:
            print(l.name)

    def light_play(self,cmd):
        self.keyword_identified = 0
        self.voice.play('pi-response')
        return self.keyword_identified
