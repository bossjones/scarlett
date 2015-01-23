# -*- coding: UTF-8 -*-

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
import subprocess
import pygst
pygst.require("0.10")
import gst
import pygtk
pygtk.require('2.0')
import gtk
from scarlett.basics import *
from scarlett.constants import *

import gobject
gobject.threads_init()

# Create a gtreamer playerbin
__PLAYER__ = None

# Connect End Of Stream handler on bus
main_loop = gobject.MainLoop()
def eos_handler(bus, message):
    __PLAYER__.set_state(gst.STATE_READY)
    main_loop.quit()


def play(sound):
    """
    Play a sound.
    """
    scarlett.log.debug(Fore.YELLOW + 'PWD: ' + PWD)
    scarlett.log.debug(Fore.YELLOW + 'SOUND: ' + sound)
    global __PLAYER__

    # Create player once
    if __PLAYER__ is None:
        __PLAYER__ = gst.element_factory_make("playbin2", "player")

        # Connect End Of Stream handler on bus
        bus = __PLAYER__.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', eos_handler)

    # Stop previous play if any
    else:
        __PLAYER__.set_state(gst.STATE_READY)

    filename = '%s/static/sounds/%s.wav' % (PWD, sound)

    # Play file
    __PLAYER__.set_property('uri', 'file://%s' % filename)
    __PLAYER__.set_state(gst.STATE_PLAYING)


def play_block(sound):
    """
    Play sound but block until end
    """
    #scarlett.log.debug(Fore.YELLOW + '%s ' + __name__)
    global main_loop

    # Play sound
    play(sound)

    # Wait for EOS signal in mail loop
    main_loop.run()


def play_free():
    """
    Free player resource
    """
    global __PLAYER__

    # Delete player
    if __PLAYER__ is not None:
        __PLAYER__.set_state(gst.STATE_NULL)
        __PLAYER__ = None

class Voice(ScarlettBasics):

    def __init__(self, brain):
        super(Voice, self).__init__(brain)
        self.brain = brain
        self.config = scarlett.config
        self.sudo_enabled = self.config.getboolean('speech', 'sudo_enabled')
        self.reading_speed = 165

    # best sounding female voice: espeak -ven+f3 -k5 -s150 "hello malcolm"
    def speak(self, text, speed=150):
        text = ''.join(e for e in text if e.isalpha() or e.isspace())
        if self.sudo_enabled:
            subprocess.Popen('sudo espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text), shell=True).wait()
        else:
            subprocess.Popen('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text), shell=True).wait()

    def greetings_play(self):
        self.speak(
            "Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands")

    def read(self, text):
        self.speak(text, self.reading_speed)

