#!/usr/bin/env python

"""
Scarlett Client Utils
"""
import scarlett
import os
import sys
import time
import getopt
import tempfile
import json
import glob
import tempfile
import subprocess
import pygtk
pygtk.require('2.0')
import gtk
import gobject
import pygst
pygst.require('0.10')
gobject.threads_init()
import gst
from scarlett.basics import *
from scarlett.constants import *

__PLAYER__ = gst.element_factory_make("playbin", "player")

class Voice(ScarlettBasics):

    def __init__(self,brain):
        super(Voice, self).__init__(brain)
        self.brain = brain
        self.config = scarlett.config
        self.sudo_enabled = self.config.getboolean('speech', 'sudo_enabled')
        self.reading_Speed = 165
        # ScarlettBasics.__init__(self)

    # """
    # In the near future we will test this function here to see if it works better than the current one
    # """
    # def say(self,something, language='en', voice='f3'):
    #     subprocess.call(['espeak', '-v%s+%s' % (language, voice), something])

    # best sounding female voice: espeak -ven+f3 -k5 -s150 "hello malcolm"
    def speak(self, text, speed=150):
        # lets add this back in later
        # NOTE: old command by josip ( mmj2f 8:55AM March 15, 2014 )
        # remove special characters first
        text = ''.join(e for e in text if e.isalpha() or e.isspace())
        if self.sudo_enabled:
            os.system('sudo espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))
        else:
            os.system('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text))

    def greetings_play(self):
        self.speak(
            "Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands")

    def read(self, text):
        self.speak(text, self.reading_Speed)

    def play(self, sound):
        scarlett.log.debug(Fore.YELLOW + 'PWD: ' + PWD)
        scarlett.log.debug(Fore.YELLOW + 'SOUND: ' + sound)
        global __PLAYER__
        __PLAYER__.set_state(gst.STATE_NULL)
        __PLAYER__ = gst.element_factory_make("playbin", "player")
        __PLAYER__.set_property(
            'uri', 'file://%s/static/sounds/%s.wav' %
            (PWD, sound))
        __PLAYER__.set_state(gst.STATE_PLAYING)
