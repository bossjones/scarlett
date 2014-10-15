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

"""
Implements Feature related API. Allows for certain features
to be called based on what is in config.

To define a new feature just subclass Feature, like this.

class AuthFeature(Feature):
  pass

Then start creating subclasses of your new plugin.

class MyFancyAuth(AuthFeature):
  capability = ['spotify', 'datadog']

The actual interface is duck typed.

"""

class Feature(object):

    def __init__(self,name):

        self.name   = name

    def getName(self):

        return self.name

    def __str__(self):

        return "Scarlett Feature is %s" % (self.name)

    def general_play(self,cmd):
      self.keyword_identified = 0
      self.voice.play('pi-cancel')

    def module_exists(self,module_name):
        try:
            __import__(module_name)
        except ImportError:
            return False
        else:
            return True
