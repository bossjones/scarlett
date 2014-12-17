#!/usr/bin/env python

import scarlett
from scarlett.features import *
from phue import Bridge
import socket
import time
import os


class FeatureHueLights(Feature):

    capability = []

    def __init__(self, voice, brain, *args, **kwargs):
        super(FeatureHueLights, self).__init__(args, kwargs)
        self._light_objects = []
        self._name = "hue"
        self.voice = voice
        self.brain = brain
        self.hue_config = os.path.join(expanduser('~'), '.python_hue')
        self.hue_bridge = "{0}".format(scarlett.config.get('hue', 'bridge'))

        # add test for unauthorized user
        # [{u'error': {u'address': u'/',
        # u'description': u'unauthorized user',
        # u'type': 1}}]

        try:
            self.b = Bridge(
                ip=self.hue_bridge,
                config_file_path=self.hue_config)
        except socket.error:  # Error connecting using Phue
            scarlett.log.debug(
                Fore.YELLOW +
                "Sorry, had an issue connecting to phue Bridge, make sure you register the app first")

        self.api = self.b.get_api()
        self.lights = self.api.get('lights')

        # capture all lights currently configured
        for light_obj in self.b.get_light_objects():
            self._light_objects.append(light_obj)

    def find_active_lights(self):
        pass

    @property
    def name(self):
        return self._name

    def find_light(self, light_name):
        return self._light_objects[light_name]

    def get_light_names(self):
        self.light_play()
        lights_list = self.b.get_light_objects('list')
        for light in lights_list:
            self.voice.speak(light.name)
            time.sleep(2)

    def brighten_light(self, light_name):
        self._light_objects[light_name].on = True
        self._light_objects[light_name].brightness = 240
        return self._light_objects[light_name].brightness

    def turn_on_all_lights(self):
        lights_list = self.b.get_light_objects('list')
        for light in lights_list:
            light.on = True
            light.colortemp = 400
            light.bri = 127

    def brighten_lights_all(self, light_name):
        lights_list = self._light_objects
        for light in lights_list:
            light.on = True
            light.brightness = 240

    def darken_light(self, light_name):
        self._light_objects[light_name].on = True
        self._light_objects[light_name].brightness = 100
        return self._light_objects[light_name].brightness

    def print_light_names(self):
        for l in self.lights:
            scarlett.log.debug(Fore.YELLOW + "" + (l.name))

    def light_play(self, cmd="hue_lights"):
        self.voice.play('pi-response')
        self.failed = int(self.brain.set_brain_item_r('scarlett_failed', 0))
        self.keyword_identified = int(
            self.brain.set_brain_item_r(
                'scarlett_main_keyword_identified',
                0))
