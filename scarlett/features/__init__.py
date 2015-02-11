# -*- coding: UTF-8 -*-

import scarlett
from scarlett.constants import *


class Feature(object):

    def __init__(self, voice, brain):
        self.voice = voice
        self.brain = brain

    @property
    def name(self):
        return self._name

    def __str__(self):
        return "Scarlett Feature is %s" % (self.name)

    def module_exists(self, module_name):
        try:
            __import__(module_name)
        except ImportError:
            return False
        else:
            return True
