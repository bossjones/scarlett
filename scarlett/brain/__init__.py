#!/usr/bin/env python

"""
Scarlett Brain
"""

import scarlett
from scarlett.constants import *

class ScarlettBrain(object):

    def __init__(self,name):
      self.config       = scarlett.config
      self._name   = name

    @property
    def name(self):
        return self._name

    def __str__(self):

        return "Scarlett Brain name is %s" % (self.name)
