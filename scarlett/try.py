#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Run examples:
# python try.py --core-feature="brain"
# python try.py --core-feature="player"
# python try.py --core-feature="speaker"
# python try.py --core-feature="listener"

import pkgutil
import sys
import os
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import signal
gobjectnotimported = False

try:
    import dbus
    import dbus.service
    from dbus.mainloop.glib import DBusGMainLoop
    from dbus.mainloop.glib import threads_init
    import subprocess
    from subprocess import call
    import gobject
    # Initialize gtk threading
    gobject.threads_init()
    # If the keyword argument set_as_default is given and is true, set the new
    # main loop as the default for all new Connection or Bus instances.
    threads_init()
    DBusGMainLoop(set_as_default=True)
    import pygst
    pygst.require('0.10')
    # gobject.threads_init()
    # threads_init()
    import scarlett
    from scarlett.constants import *
    from scarlett import __version__
    from scarlett import ScarlettSystem
    #import scarlett.basics.voice
    #from scarlett.basics.voice import Voice
    #import scarlett.bootstrap
    #from scarlett.listener.gstlisteneri import GstListenerImproved
    #from scarlett.basics.talk import ScarlettTalk
    #import scarlett.basics.say as scarlett_says
except:
    gobjectnotimported = True

import argparse

from IPython.core.debugger import Tracer
from IPython.core import ultratb
sys.excepthook = ultratb.FormattedTB(mode='Verbose',
                                     color_scheme='Linux', call_pdb=True, ostream=sys.__stdout__)

from colorlog import ColoredFormatter

import logging


def setup_logger():
    """Return a logger with a default ColoredFormatter."""
    formatter = ColoredFormatter(
        "(%(threadName)-9s) %(log_color)s%(levelname)-8s%(reset)s %(message_log_color)s%(message)s",
        datefmt=None,
        reset=True,
        log_colors={
            'DEBUG':    'cyan',
            'INFO':     'green',
            'WARNING':  'yellow',
            'ERROR':    'red',
            'CRITICAL': 'red',
        },
        secondary_log_colors={
            'message': {
                'ERROR':    'red',
                'CRITICAL': 'red',
                'DEBUG': 'yellow'
            }
        },
        style='%'
    )

    logger = logging.getLogger(__name__)
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    return logger


def set_dbus_launch_shell():
    # source:
    # http://stackoverflow.com/questions/2143785/python-dbus-session-bus-x11-dependency
    p = subprocess.Popen('dbus-launch',
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)

    print "p: {}".format(p)

    for var in p.stdout:
        sp = var.split('=', 1)
        print sp
        os.environ[sp[0]] = sp[1][:-1]


def main():
    """Create and use a logger."""
    logger = setup_logger()

    CORE_MODULES = {
        'brain': {
            'module_path': 'scarlett.brain.',
            'module_name': 'scarlettbrainfsm'
        },
        'player': {
            'module_path': 'scarlett.basics.',
            'module_name': 'say'
        },
        'speaker': {
            'module_path': 'scarlett.basics.',
            'module_name': 'speakerfsm'
        },
        'listener': {
            'module_path': 'scarlett.listener.',
            'module_name': 'gstlistenerfsm'
        }
    }

    parser = argparse.ArgumentParser()
    parser.add_argument("--core-feature", default="brain")

    scarlett_cli_args = parser.parse_args()

    feature_name = scarlett_cli_args.core_feature

    # scarlett.brain.scarlettbrainfsm.scarlettbraini
    folder_name = CORE_MODULES[feature_name]['module_path'].split('.')[1]
    module_name = CORE_MODULES[feature_name]['module_name']

    module_paths = '{}'.format(CORE_MODULES[feature_name]['module_path'])
    potential_paths = 'scarlett.{}.{}'.format(folder_name, module_name)

    if feature_name == 'brain':
        modules = pkgutil.iter_modules(scarlett.brain.__path__, module_paths)
    elif feature_name == 'speaker':
        modules = pkgutil.iter_modules(scarlett.basics.__path__, module_paths)
    elif feature_name == 'player':
        modules = pkgutil.iter_modules(scarlett.basics.__path__, module_paths)
    elif feature_name == 'listener':
        modules = pkgutil.iter_modules(
            scarlett.listener.__path__, module_paths)
    else:
        logger.debug("Error loading {}.".format(feature_name))

    for module_loader, mod_name, ispkg in modules:

        if mod_name not in sys.modules and mod_name == potential_paths:

            logger.debug("potential_paths: " + potential_paths + "\n")
            logger.debug("modules: ")
            logger.debug(modules)
            logger.debug("\n")

            logger.debug("mod_name: \n")
            logger.debug(mod_name)
            logger.debug("\n")

            logger.debug(mod_name == potential_paths)
            logger.debug(mod_name)
            logger.debug(potential_paths)
            #try:
                # Import module
                # eg: scarlett.brain.scarlettbrainfsm
            loaded_mod = importlib.import_module(potential_paths)

            # Load class from imported module
            # eg: ScarlettBrainFSM
            class_name = loaded_mod
            logger.debug(class_name)

            loaded_class = getattr(loaded_mod, 'setup_core')(None)

            # Create an instance of the class
            instance = loaded_class
            #Tracer()()
            logger.debug(instance)

            #except ImportError:
            #    logging.error('Failed to import')
            #    raise

                # Tracer()()

            instance.start()
            instance.hello()

            if feature_name == 'speaker':
                instance.event_speak(('scarlett_speak',
                                      'Hello sir. How are you doing this afternoon? I am full lee function nall, andd red ee for your commands'))

            # if instance.exc_info:
            #    raise instance.exc_info[1], None, instance.exc_info[2]
            # return instance.result


if __name__ == '__main__':
    set_dbus_launch_shell()

    main()
