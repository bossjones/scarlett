# -*- coding: utf-8 -*-

from scarlett.core.config import Config, ScarlettConfigLocations
import datetime
import os
import platform
from colorlog import ColoredFormatter
import logging
import logging.config
import scarlett.errors
import threading

# NOTE: take from scarlett_improved

try:
    import dbus
    import dbus.service
    from dbus.mainloop.glib import DBusGMainLoop
    from dbus.mainloop.glib import threads_init
    import gobject
    # Initialize gtk threading
    gobject.threads_init()
    # If the keyword argument set_as_default is given and is true, set the new
    # main loop as the default for all new Connection or Bus instances.
    threads_init()
    DBusGMainLoop(set_as_default=True)
    import pygst
    pygst.require('0.10')
    import scarlett.constants
    from scarlett.constants import (
        EVENT_CALLBACK,
        EVENT_SERVICE,
        EVENT_STATE,
        EVENT_TIME,
        EVENT_DEFAULT,
        EVENT_SCARLETT_START,
        EVENT_SCARLETT_STOP,
        EVENT_STATE_CHANGED,
        EVENT_TIME_CHANGED,
        EVENT_CALL_SERVICE,
        EVENT_SERVICE_EXECUTED,
        EVENT_SERVICE_REGISTER,
        EVENT_PLATFORM_DISCOVERED,
        EVENT_SCARLETT_SAY,
        EVENT_BRAIN_UPDATE,
        EVENT_BRAIN_CHECK
    )

except:
    gobjectnotimported = True

import textwrap
from functools import wraps
import time

import pprint

import redis
from scarlett.brain.scarlettbraini import ScarlettBrainImproved

import scarlett.util as util

# Define number of MINIMUM worker threads.
# During bootstrap of HA (see bootstrap.from_config_dict()) worker threads
# will be added for each component that polls devices.
MIN_WORKER_THREAD = 2

import ast

# drops you down into pdb if exception is thrown
import sys

from colorama import init, Fore, Back, Style

# chg: When we enable this, scarlett runner stops working
# import scarlett.basics.speakerfsm

# set colorama
init(autoreset=True)

__author__ = 'Malcolm Jones'
__email__ = 'bossjones@theblacktonystark.com'
__version__ = '0.5.0'
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


def create_worker_pool():
    """ Creates a worker pool to be used. """

    def job_handler(job):
        """ Called whenever a job is available to do. """
        try:
            func, arg = job
            func(arg)
        except Exception:  # pylint: disable=broad-except
            # Catch any exception our service/event_listener might throw
            # We do not want to crash our ThreadPool
            scarlett.log.exception("BusHandler:Exception doing job")

    def busy_callback(worker_count, current_jobs, pending_jobs_count):
        """ Callback to be called when the pool queue gets too big. """

        scarlett.log.warning(
            "WorkerPool:All %d threads are busy and %d jobs pending",
            worker_count, pending_jobs_count)

        for start, job in current_jobs:
            scarlett.log.warning("WorkerPool:Current job from %s: %s",
                                 util.datetime_to_str(start), job)

    return util.ThreadPool(job_handler, MIN_WORKER_THREAD, busy_callback)


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

        # These will later be populated w/ scarlett core objects in the
        # ./bin/scarlett_improved
        self.brain = None
        self.player = None
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

        self._lock = threading.Lock()

        self._pool = scarlett.create_worker_pool()

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
                               "RECIEVED: {} from time-started: {}".format(
                                   event['event_type'], event['data'])
                               )
        elif event['event_type'] == 'listener_hyp':
            scarlett.log.debug(Fore.GREEN +
                               "RECIEVED: {} from listener-hyp: {}".format(
                                   event['event_type'], event['data'])
                               )
            # TODO: Turn this into self.commander.check_cmd(hyp)
        elif event['event_type'] == 'scarlett_speak':
            scarlett.log.debug(Fore.GREEN +
                               "RECIEVED: {} from scarlett-speak: {}".format(
                                   event['event_type'], event['data'])
                               )
            # TODO: YOU NEED THIS LOCK TO WORK ETC
            with self._lock:
                scarlett.log.info('Adding job {}'.format(scarlett.constants.EVENT_SERVICE))
                # self._pool.add_job(scarlett.constants.EVENT_SERVICE,
                #                    (self._execute_service,
                #                     (scarlett.basics.speakerfsm.say_block,
                #                      event['data'])))

        else:
            raise ValueError('Unknown scarlettTime message: {}'.format(event))

    def _execute_service(self, service_and_call):
        """ Executes a service and fires a SERVICE_EXECUTED event. """
        service, call = service_and_call

        service(call)

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
        self.loop.quit()  # OLD # gobject.mainloop.quit()

    @dbus.service.method("org.scarlettapp.scarlettdaemon",
                         in_signature='', out_signature='')
    def Exit(self):
        scarlett.log.debug(Fore.YELLOW + "Exit signal occurred")
        self.remove_from_connection()
        self.loop.quit()
