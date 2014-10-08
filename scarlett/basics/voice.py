#!/usr/bin/env python

"""
Scarlett Client Utils
"""
import os
from scarlett.basics import *

# DISABLED 10/7/2014 # SUDO_ENABLED       = scarlett.config.getboolean('speech','sudo_enabled')
# DISABLED 10/7/2014 # READING_SPEED      = 165
# DISABLED 10/7/2014 # PWD                = os.path.dirname(os.path.abspath(__file__ + '/..'))

class Voice(ScarlettBasics):

  def __init__(self, gobject, gst, config):
    self.keyword_identified = 0
    self.sudo_enabled       = self.config.getboolean('speech','sudo_enabled')
    self.reading_Speed      = 165
    self.config             = config

  # best sounding female voice: espeak -ven+f3 -k5 -s150 "hello malcolm"
  #@staticmethod
  def speak(self, text, speed=150):
    # lets add this back in later
    # NOTE: old command by josip ( mmj2f 8:55AM March 15, 2014 )
    # remove special characters first
    text = ''.join(e for e in text if e.isalpha() or e.isspace())
    if self.sudo_enabled:
      os.system('sudo espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))
    else:
      os.system('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))

  #@staticmethod
  def greetings_play(self):
    self.speak("Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands")

  def read(self, text):
    self.speak(text, self.reading_Speed)

  __PLAYER__ = gst.element_factory_make("playbin", "player")
  #@staticmethod
  def play(self, sound):
    global __PLAYER__
    __PLAYER__.set_state(gst.STATE_NULL)
    __PLAYER__ = gst.element_factory_make("playbin", "player")
    __PLAYER__.set_property('uri', 'file://%s/static/sounds/%s.wav' % (PWD, sound))
    __PLAYER__.set_state(gst.STATE_PLAYING)
