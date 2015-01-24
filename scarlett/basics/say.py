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

# Create a gtreamer espeak
__ESPEAK__ = None

# Connect End Of Stream handler on bus
main_loop = gobject.MainLoop()
def eos_handler(bus, message):
    __ESPEAK__.set_state(gst.STATE_READY)
    main_loop.quit()


def say(sound):
    """
    Play a sound.
    """
    scarlett.log.debug(Fore.YELLOW + 'PWD: ' + PWD)
    scarlett.log.debug(Fore.YELLOW + 'SOUND: ' + sound)
    global __ESPEAK__

    # Create player once
    if __ESPEAK__ is None:
        espk_pipeline = 'espeak name=source ! autoaudiosink'
        __ESPEAK__ = gst.parse_launch(espk_pipeline)

        # Connect End Of Stream handler on bus
        bus = __ESPEAK__.get_bus()
        bus.add_signal_watch()
        bus.connect('message::eos', eos_handler)
        bus.connect('message::error', eos_handler)

    # Stop previous play if any
    else:
        __ESPEAK__.set_state(gst.STATE_READY)

    #filename = '%s/static/sounds/%s.wav' % (PWD, sound)

    # Play file
    source = __ESPEAK__.get_by_name("source")
    #source.set_property("text","{}".format(sound))
    #source.set_property("rate",165)

    source.props.pitch = 50
    source.props.rate = 165
    source.props.voice = "en+f3"
    source.props.text = sound;

    #subprocess.Popen('espeak -ven+f3 -k5 -s%d "%s" 2>&1' % (speed, text), shell=True).wait()


    __ESPEAK__.set_state(gst.STATE_PLAYING)


def say_block(sound):
    """
    Play sound but block until end
    """
    global main_loop

    # Play sound
    say(sound)

    # Wait for EOS signal in mail loop
    main_loop.run()


def say_free():
    """
    Free player resource
    """
    global __ESPEAK__

    # Delete player
    if __ESPEAK__ is not None:
        __ESPEAK__.set_state(gst.STATE_NULL)
        __ESPEAK__ = None
