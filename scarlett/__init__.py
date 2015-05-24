# -*- coding: utf-8 -*-

from scarlett.core.config import Config, ScarlettConfigLocations
#### DISABLED UNTIL READY # import scarlett.plugin
import datetime
import os
import platform
import logging
import logging.config
import scarlett.errors

# NOTE: take from scarlett_imporved

try:
    import dbus
    import dbus.service
    from dbus.mainloop.glib import DBusGMainLoop
    from dbus.mainloop.glib import threads_init
    import gobject
    # Initialize gtk threading
    gobject.threads_init()
    # If the keyword argument set_as_default is given and is true, set the new main loop as the default for all new Connection or Bus instances.
    threads_init()
    DBusGMainLoop(set_as_default=True)
    import pygst
    pygst.require('0.10')
    from scarlett.constants import *
    from scarlett import __version__
except:
    gobjectnotimported = True

import textwrap
from functools import wraps
import time

import pprint

import redis
from scarlett.brain.scarlettbraini import ScarlettBrainImproved

import ast

# drops you down into pdb if exception is thrown
import sys

__author__  = 'Malcolm Jones'
__email__   = 'bossjones@theblacktonystark.com'
__version__ = '0.4.0'
Version = __version__  # for backware compatibility

# http://bugs.python.org/issue7980
datetime.datetime.strptime('', '')

UserAgent = 'Scarlett/%s Python/%s %s/%s' % (
    __version__,
    platform.python_version(),
    platform.system(),
    platform.release()
)

config = Config()


def init_logging():
    for file in ScarlettConfigLocations:
        try:
            logging.config.fileConfig(os.path.expanduser(file))
        except:
            pass


class NullHandler(logging.Handler):

    def emit(self, record):
        pass

log = logging.getLogger('scarlett')
perflog = logging.getLogger('scarlett.perf')
log.addHandler(NullHandler())
perflog.addHandler(NullHandler())
init_logging()

# convenience function to set logging to a particular file


def set_file_logger(name, filepath, level=logging.INFO, format_string=None):
    global log
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.FileHandler(filepath)
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log = logger


def set_stream_logger(name, level=logging.DEBUG, format_string=None):
    global log
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s]:%(message)s"
    logger = logging.getLogger(name)
    logger.setLevel(level)
    fh = logging.StreamHandler()
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    log = logger

class ScarlettSystemException(dbus.DBusException):
    _dbus_error_name = 'org.scarlettapp.scarlettbotexception'

class ScarlettSystem(dbus.service.Object):
    """ Actual scarlett bot object that has a brain, voice, etc """

    DBUS_NAME = 'org.scarlettapp.scarlettdaemon'
    DBUS_PATH = '/org/scarlettapp/scarlettdaemon'

    _scarlett_services = []

    def __init__(self):

        bus_name = dbus.service.BusName(
            ScarlettSystem.DBUS_NAME,
            bus=dbus.SessionBus()
            )

        dbus.service.Object.__init__(
            self,
            bus_name,
            ScarlettSystem.DBUS_PATH
            )

        self.loop = None
        # DISABLED FOR NOW # self.pool = pool = create_worker_pool()

        # These will later be populated w/ scarlett core objects in the ./bin/scarlett_improved
        self.brain   = None
        self.player  = None
        self.speaker = None

        scarlett.set_stream_logger('scarlett')

        self.scarlett_version_info = textwrap.dedent('''\
                                           Scarlett {version} ({platform})
                                           Python {pymajor}.{pyminor}.{pymicro}
                                           PyGst {pygst_version}
                                           Gobject {gobject_version}
                                           '''.format(
                                            version=__version__,
                                            platform=sys.platform,
                                            pymajor=sys.version_info.major,
                                            pyminor=sys.version_info.minor,
                                            pymicro=sys.version_info.micro,
                                            pygst_version=pygst._pygst_version,
                                            gobject_version=gobject.gobject.glib_version
                                            ))

        scarlett.log.debug(
            Fore.GREEN +
            "VERSION INFO: \n\n" +
            self.scarlett_version_info
            )

        # reserved for things like scarlett's brain, listener, player, speaker
        self.base_services = []

        self.features = []

        ### DISABLED FOR NOW # self._brain = ScarlettBrainImproved(
        ### DISABLED FOR NOW #     host=scarlett.config.get('redis', 'host'),
        ### DISABLED FOR NOW #     port=scarlett.config.get('redis', 'port'),
        ### DISABLED FOR NOW #     db=scarlett.config.get('redis', 'db')
        ### DISABLED FOR NOW #     )

        #scarlett.log.debug(Fore.GREEN + "Scarlett Creating Voice Object")

        #scarlett.basics.voice.play_block('pi-listening')

        #scarlett_says.say_block("helllllllllllloooo")

        #self.listener = GstListenerImproved("gst", self._brain, self._voice, False)

    def connect_features(self):
        scarlett.log.info(Fore.GREEN + "would connect feature")
        pass

    def scarlett_event_cb(self, scarlett_obj, message):
        """Handle message send by webbrowser.

        :param scarlett_obj: ServiceFeature obj that sent the message
        :type scarlett_obj: scarlett.Feature
        :param message: Message containing event data
        :type message: dict

        """
        scarlett.log.debug(Fore.GREEN + "(service -> gtk) %s", message)

        # NOTE: ast.literal_eval raises an exception if the input isn't a
        # valid Python datatype, so the code won't be executed if it's not.
        # NOTE: Use ast.literal_eval whenever you need eval. If you
        # have Python expressions as an input that you want to
        # evaluate, you shouldn't (have them).
        event = ast.literal_eval(message)

        scarlett.log.debug(Fore.GREEN + "Bus:Handling %s",
            event['event_type'])

        if event['event_type'] == 'service_state':
           scarlett.log.debug(Fore.GREEN +
                "RECIEVED: {} from time-started: {}".format(event['event_type'],event['data']))
        else:
            raise ValueError('Unknown scarlettTime message: {}'.format(event))

    @dbus.service.method('org.scarlettapp.scarlettdaemon',
        in_signature='', out_signature='')
    def main(self):
        """Main method used to start scarlett application."""
        # All PyGTK applications must have a gtk.main(). Control ends here
        # and waits for an event to occur (like a key press or mouse event).
        # OLD # gtk.main()
        # DISABLED FOR NOW # scarlett.log.info(Fore.GREEN +
        #    "Starting Home Assistant (%d threads)", self.pool.worker_count)

        self.loop = gobject.MainLoop()

        try:
          self.loop.run()
        except KeyboardInterrupt:
            self.Exit()

    @dbus.service.method('org.scarlettapp.scarlettdaemon',
        in_signature='', out_signature='')
    def destroy(self):
        scarlett.log.debug(Fore.YELLOW + "Destroy signal occurred")
        self.remove_from_connection()
        self.loop.quit() # OLD # gobject.mainloop.quit()

    @dbus.service.method("org.scarlettapp.scarlettdaemon",
                         in_signature='', out_signature='')
    def Exit(self):
        scarlett.log.debug(Fore.YELLOW + "Exit signal occurred")
        self.remove_from_connection()
        self.loop.quit()




