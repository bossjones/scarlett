# -*- coding: UTF-8 -*-

"""
Scarlett Client Utils
"""

import scarlett
import pygst
pygst.require("0.10")
import gst
import pygtk
pygtk.require('2.0')
from scarlett.basics import *
from scarlett.constants import *

import gobject
gobject.threads_init()

from gettext import gettext as _

SCARLETT_ROLE = 'speaker'

# Create a gtreamer espeak
__ESPEAK__ = None

# Connect End Of Stream handler on bus
main_loop = gobject.MainLoop()
def eos_handler(bus, message):
    __ESPEAK__.set_state(gst.STATE_READY)
    main_loop.quit()

def gstmessage_cb(bus, message, __ESPEAK__):
    if message.type in (gst.MESSAGE_EOS, gst.MESSAGE_ERROR):
        __ESPEAK__.set_state(gst.STATE_NULL)

def say(sound):
    """
    Play a sound.
    """
    scarlett.log.debug(Fore.YELLOW + 'PWD: ' + PWD)
    scarlett.log.debug(Fore.YELLOW + 'SOUND: ' + sound)
    global __ESPEAK__

    # Create espeak once
    if __ESPEAK__ is None:
        espk_pipeline = 'espeak name=source ! autoaudiosink'
        __ESPEAK__ = gst.parse_launch(espk_pipeline)

        # Connect End Of Stream handler on bus
        bus = __ESPEAK__.get_bus()
        bus.add_signal_watch()
        bus.connect('message', gstmessage_cb, __ESPEAK__)
        bus.connect('message::eos', eos_handler)
        bus.connect('message::error', eos_handler)

    # Stop previous espeak if any
    else:
        __ESPEAK__.set_state(gst.STATE_READY)

    # Play file
    source = __ESPEAK__.get_by_name("source")

    ####################################################################################
    # all writable properties(including text) make sense only at start playing;
    # to apply new values you need to stop pipe.set_state(gst.STATE_NULL) pipe and
    # start it again with new properties pipe.set_state(gst.STATE_PLAYING).
    # source: http://wiki.sugarlabs.org/go/Activity_Team/gst-plugins-espeak
    ####################################################################################
    source.props.pitch = 50
    source.props.rate = 100
    source.props.voice = "en+f3"
    source.props.text = _('{}'.format(sound))

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
    Free espeak resource
    """
    global __ESPEAK__

    # Delete espeak
    if __ESPEAK__ is not None:
        __ESPEAK__.set_state(gst.STATE_NULL)
        __ESPEAK__ = None
