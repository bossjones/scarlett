#!/usr/bin/env python
"""
Scarlett Client Utils
"""

import scarlett
from scarlett import config
import os
import subprocess
import sys
import re
import scarlett.plugin
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst

SUDO_ENABLED       = False
READING_SPEED      = 165
PWD                = os.path.dirname(os.path.abspath(__file__ + '/..'))

class Voice:
  def __init__(self, gobject, gst):
    self.keyword_identified = 0

# best souning female voice: espeak -ven+f3 -k5 -s150 "hello malcolm"
def speak(text, speed=150):
  # lets add this back in later
  # NOTE: old command by josip ( mmj2f 8:55AM March 15, 2014 )
  # remove special characters first
  text = ''.join(e for e in text if e.isalpha() or e.isspace())
  if SUDO_ENABLED:
    os.system('sudo espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))
  else:
    os.system('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))

def read(text):
  speak(text, READING_SPEED)

__PLAYER__ = gst.element_factory_make("playbin", "player")
def play(sound):
  global __PLAYER__
  __PLAYER__.set_state(gst.STATE_NULL)

  __PLAYER__ = gst.element_factory_make("playbin", "player")
  __PLAYER__.set_property('uri', 'file://%s/static/sounds/%s.wav' % (PWD, sound))
  __PLAYER__.set_state(gst.STATE_PLAYING)
