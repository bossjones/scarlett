# -*- coding: UTF-8 -*-

"""
Scarlett Say, THIS IS WHAT WE WANT TO BASE EVERYTHING OFF OF
"""

import scarlett
import pygst
pygst.require("0.10")
import gst
import pygtk
pygtk.require('2.0')
import gobject
gobject.threads_init()
import dbus
import dbus.service

# TODO: Figure out if we need this or not, re dbus threading
# from dbus.mainloop.glib import DBusGMainLoop
# dbus_loop = DBusGMainLoop(set_as_default=True)
# dsession = SessionBus(mainloop=dbus_loop)

dbus.mainloop.glib.threads_init()
import gst
import os
import threading
import time
import logging
from transitions import Machine

from scarlett.events import scarlett_event

from gettext import gettext as _
from Queue import Queue

# Create a gtreamer espeak
# __ESPEAK__ = None

# Connect End Of Stream handler on bus
# main_loop = gobject.MainLoop()

SCARLETT_ROLE = 'speaker'
CORE_OBJECT = 'SpeakerFSM'

_INSTANCE = None

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) [%(module)s] %(message)s',)


def setup_core(ss):

    logging.info("attempting to setup SpeakerFSM")

    global _INSTANCE

    if _INSTANCE is None:
        _INSTANCE = SpeakerFSM()
    return _INSTANCE

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
    scarlett.log.debug('PWD: ' + PWD)
    scarlett.log.debug('SOUND: ' + sound)
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

    ##########################################################################
    # all writable properties(including text) make sense only at start playing;
    # to apply new values you need to stop pipe.set_state(gst.STATE_NULL) pipe and
    # start it again with new properties pipe.set_state(gst.STATE_PLAYING).
    # source: http://wiki.sugarlabs.org/go/Activity_Team/gst-plugins-espeak
    ##########################################################################
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


class SpeakerFSM(gobject.GObject):

    __gproperties__ = {
        'speech_text': (
            gobject.TYPE_STRING,  # type
            'Speech Text',  # nick name
            # description
            'Speech for Scarlett to say via espeak',
            '',  # default value
            gobject.PARAM_READWRITE
        ),
        'override_parse': (
            gobject.TYPE_STRING,  # type
            'Override parse',  # nick name
            # description
            'Allows you to override what the gst parse line looks like',
            '',  # default value
            gobject.PARAM_READWRITE
        ),
        'canceled': (
            gobject.TYPE_BOOLEAN,  # type
            'Canceled run',  # nick name
            'Drop out of loop when finished',  # description
            False,  # default value
            gobject.PARAM_READWRITE
        ),
        'action': (
            gobject.TYPE_STRING,  # type
            'Speech Action',  # nick name
            # description
            'Set if speaker should be running or waiting',
            'scarlett_no_speak',  # default value
            gobject.PARAM_READWRITE
        )
    }

    __gsignals__ = {
        'speaker-started': (
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING,)
        ),
        'speaking': (
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING,)
        ),
        'fin-speaking': (
            gobject.SIGNAL_RUN_LAST,
            gobject.TYPE_NONE,
            (gobject.TYPE_STRING,)
        )
    }

    capability = []

    states = ['initalize', 'ready', 'speaking',
              'fin-speaking']

    DBUS_NAME = 'org.scarlettapp.scarlettdaemon'
    DBUS_PATH = '/org/scarlettapp/scarlettdaemon'

    def __init__(self, *args, **kwargs):

        gobject.GObject.__init__(self)

        # managed by gproperties
        self.override_parse = ''
        self.speech_text = ''
        self.loop = None
        self.config = scarlett.config
        self.name = 'SpeakerFSM'
        self.canceled = False
        self.queue = Queue()

        # scarlett_speak, scarlett_no_speak
        self.action = 'scarlett_no_speak'

        # Initalize the state machine
        self.machine = Machine(
            model=self,
            states=self.states,
            initial='initalize')

        # startup transition
        self.machine.add_transition(
            trigger='startup',
            source='initalize',
            dest='ready')

        # array / dict of state machines connected to scarlett
        self._machines = {}

        # Check interval, in seconds
        self.interval = 1

        # self.parse_launch_array = self._get_espeak_definition(
        #     self.override_parse)

        # self.espeak_pipeline = gst.parse_launch(
        #     ' ! '.join(self.parse_launch_array))

        ss_speaker = threading.Thread(
            name='Scarlett Speaker', target=self.go)
        ss_speaker.daemon = True
        ss_speaker.start()

    def do_get_property(self, property):
        if property.name == 'speech-test':
            return self.speech_text
        elif property.name == 'override-parse':
            return self.override_parse
        elif property.name == 'canceled':
            return self.canceled
        else:
            raise AttributeError('unknown property %s' % property.name)

    def do_set_property(self, property, value):
        if property == 'speech-text':
            self.speech_text = value
        elif property == 'override-parse':
            self.override_parse = value
        elif property == 'canceled':
            self.canceled = value
        else:
            raise AttributeError('unknown property %s' % property)

    def go(self):
        global CORE_OBJECT

        logging.info("INSIDE START")

        speaker_connect = scarlett_event(
              'service_state',
              data=CORE_OBJECT
        )

        # idle_emit since this is something with low priority
        gobject.idle_add(
            self.emit,
            'speaker-started', speaker_connect
        )

        while True:
            # always expect action and text in tuple
            event_action, event_text = self.queue.get()
            if event_action == 'scarlett_speak_end':
                self.stop()
                return
            elif event_action == 'scarlett_no_speak':
                time.sleep(.1)
                continue
            elif event_action == 'scarlett_speak':

                speaker_event = scarlett_event(
                    'scarlett_speak',
                    data=event_text
                )

                gobject.idle_add(
                    self.emit,
                    'speaking', speaker_event
                )

                print "We are speaking!"
                # Connect End Of Stream handler on bus
                # set back to no speak after finished
                self.action = 'scarlett_no_speak'

    def event_speak(self, event):
        """ Listens for new events on the EventBus and puts them
            in the process queue. """
        self.queue.put(event)

    def _get_espeak_definition(self, override_parse):
        """Return ``espeak`` definition for :func:`gst.parse_launch`."""
        # default, use what we have set
        if override_parse == '':
            return [
                'espeak name=source',
                'autoaudiosink']
        else:
            return override_parse

    def start(self):
        # register service start
        register_sstart = scarlett_event("service_state",
                                         data='on'
                                         )
        self.emit('speaker-started', register_sstart)

    def stop(self):
        self.pipeline.set_state(gst.STATE_NULL)

        if self.loop is not None:
            self.loop.quit()

    def hello(self):
        print 'hello hello hello!'

# Register to be able to emit signals
gobject.type_register(SpeakerFSM)
