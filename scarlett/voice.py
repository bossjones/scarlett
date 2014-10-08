# #!/usr/bin/env python
# """
# Scarlett Client Utils
# """

# from scarlett import *
# import os
# import subprocess
# import sys
# import re
# import scarlett.plugin

# SUDO_ENABLED       = scarlett.config.getboolean('speech','sudo_enabled')
# READING_SPEED      = 165
# PWD                = os.path.dirname(os.path.abspath(__file__ + '/..'))

# class Voice(object):
#   def __init__(self, gobject, gst):
#     self.keyword_identified = 0

#   # best sounding female voice: espeak -ven+f3 -k5 -s150 "hello malcolm"
#   #@staticmethod
#   def speak(self, text, speed=150):
#     # lets add this back in later
#     # NOTE: old command by josip ( mmj2f 8:55AM March 15, 2014 )
#     # remove special characters first
#     text = ''.join(e for e in text if e.isalpha() or e.isspace())
#     if SUDO_ENABLED:
#       os.system('sudo espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))
#     else:
#       os.system('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))

#   #@staticmethod
#   def greetings_play(self):
#     self.speak("Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands")

#   def read(self, text):
#     self.speak(text, READING_SPEED)

#   __PLAYER__ = gst.element_factory_make("playbin", "player")
#   #@staticmethod
#   def play(self, sound):
#     global __PLAYER__
#     __PLAYER__.set_state(gst.STATE_NULL)
#     __PLAYER__ = gst.element_factory_make("playbin", "player")
#     __PLAYER__.set_property('uri', 'file://%s/static/sounds/%s.wav' % (PWD, sound))
#     __PLAYER__.set_state(gst.STATE_PLAYING)
