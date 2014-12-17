# This file is part of scarlett.
# Copyright 2014, Malcolm Jones.
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.

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
