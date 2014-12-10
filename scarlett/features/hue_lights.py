#!/usr/bin/env python

import scarlett
from scarlett.features import *

class FeatureHueLights(Feature):

    capability = []

    def __init__(self, voice, brain, *args, **kwargs):
        super(FeatureHueLights, self).__init__(args, kwargs)
        self._name = "hue"
        self.voice = voice
        self.brain = brain
        if self.module_exists("phue"):
            from phue import Bridge
            self.bridge_ip = scarlett.config.get('hue', 'bridge')
            self.b = Bridge(self.bridge_ip)
            self.b.connect()
            self.lights = self.b.lights

    def find_active_lights(self):
        pass

    @property
    def name(self):
        return self._name

    def find_light(self, light_name):
        return self.b.get_light(light_name)

    def brighten_light(self, light_name):
        command = {'bri': 240}
        return self.b.set_light(light_name, command)

    def turn_on_all_lights(self):
        lights_list = self.b.get_light_objects('list')
        for light in lights_list:
            light.on = True
            light.colortemp = 400
            light.bri = 127

    def brighten_lights_all(self, light_name):
        command = {'bri': 240}
        return self.b.set_light(light_name, command)

    def darken_light(self, light_name):
        command = {'bri': 100}
        return self.b.set_light(light_name, command)

    def print_light_names(self):
        for l in self.lights:
            scarlett.log.debug(Fore.YELLOW + "" + (l.name))

    def light_play(self, cmd):
        self.voice.play('pi-response')
        self.failed = int(self.brain.set_brain_item_r('scarlett_failed', 0))
        self.keyword_identified = int(
            self.brain.set_brain_item_r(
                'scarlett_main_keyword_identified',
                0))
