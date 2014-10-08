#!/usr/bin/env python
# -*- coding: utf-8 -*-

from scarlett.core.config import Config, ScarlettConfigLocations
import scarlett.plugin
import datetime
import os
import platform
import logging
import logging.config
import scarlett.errors
from scarlett.commands import *
#from scarlett.basics import Voice

__author__ = 'Malcolm Jones'
__email__ = '@bossjones'
__version__ = '0.1.0'
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

def connect_pocketsphinx():
    scarlett.log("connect_pocketsphinx")

def connect_gearman():
    scarlett.log("connect_gearman")

def connect_forecastio():
    scarlett.log("connect_forecastio")

def connect_wordnik():
    scarlett.log("connect_wordnik")

def connect_nltk():
    scarlett.log("connect_nltk")

def connect_hue():
    scarlett.log("connect_hue")

def connect_wa():
    scarlett.log("connect_wa")

@staticmethod
def log(msg):
    d = datetime.datetime.now().strftime('%y-%m-%d %H:%M:%S')
    print '[' + d + '] ' + msg


scarlett.plugin.load_plugins(config)
