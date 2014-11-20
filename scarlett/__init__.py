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


def connect_voice():
    global log
    scarlett.log.debug("connect_voice")
    from scarlett.basics.voice import Voice
    return Voice()


def connect_forecastio():
    global log
    scarlett.log.debug("connect_forecastio")
    from scarlett.features.forecast import FeatureForecast
    return FeatureForecast()


def connect_wordnik():
    global log
    scarlett.log.debug("connect_wordnik")


def connect_nltk():
    global log
    scarlett.log.debug("connect_nltk")


def connect_hue():
    global log
    scarlett.log.debug("connect_hue")
    from scarlett.features.hue_lights import FeatureHueLights
    return FeatureHueLights()


def connect_time():
    global log
    scarlett.log.debug("connect_time")
    from scarlett.features.time import FeatureTime
    return FeatureTime()


def connect_wa():
    global log
    scarlett.log.debug("connect_wa")

# def connect_redis():
###     global log
# scarlett.log.debug("connect_redis")
###     from scarlett.brain.brain_redis import ScarlettBrainRedis
###     _redis_brain = ScarlettBrainRedis("scarlett_brain")
###     redis_brain = _redis_brain.create()
# return redis_brain


def connect_brain():
    global log
    scarlett.log.debug("connect_brain")
    from scarlett.brain import ScarlettBrain
    return ScarlettBrain(brain_name="DeepThought")

# COMMENTED OUT 10/8/2014 # scarlett.plugin.load_plugins(config)

# class RequestHandler(object):
#     """Subclass this class and define `get()` or `post()` to make a handler.
#     If you want to support more methods than the standard GET/HEAD/POST, you
#     should override the class variable ``SUPPORTED_METHODS`` in your
#     `RequestHandler` subclass.
#     """
#     SUPPORTED_METHODS = ("GET", "HEAD", "POST", "DELETE", "PATCH", "PUT",
#                          "OPTIONS")

# _template_loaders = {}  # {path: template.BaseLoader}
#     _template_loader_lock = threading.Lock()
#     _remove_control_chars_regex = re.compile(r"[\x00-\x08\x0e-\x1f]")

#     def __init__(self, application, request, **kwargs):
#         super(RequestHandler, self).__init__()

#         self.application = application
#         self.request = request
#         self._headers_written = False
#         self._finished = False
#         self._auto_finish = True
# self._transforms = None  # will be set in _execute
#         self._prepared_future = None
#         self.path_args = None
#         self.path_kwargs = None
#         self.ui = ObjectDict((n, self._ui_method(m)) for n, m in
#                              application.ui_methods.items())
# UIModules are available as both `modules` and `_tt_modules` in the
# template namespace.  Historically only `modules` was available
# but could be clobbered by user additions to the namespace.
# The template {% module %} directive looks in `_tt_modules` to avoid
# possible conflicts.
#         self.ui["_tt_modules"] = _UIModuleNamespace(self,
#                                                     application.ui_modules)
#         self.ui["modules"] = self.ui["_tt_modules"]
#         self.clear()
#         self.request.connection.set_close_callback(self.on_connection_close)
#         self.initialize(**kwargs)

#     def initialize(self):
#         """Hook for subclass initialization.
#         A dictionary passed as the third argument of a url spec will be
#         supplied as keyword arguments to initialize().
#         Example::
#             class ProfileHandler(RequestHandler):
#                 def initialize(self, database):
#                     self.database = database
#                 def get(self, username):
#                     ...
#             app = Application([
#                 (r'/user/(.*)', ProfileHandler, dict(database=database)),
#                 ])
#         """
#         pass

#     @property
#     def settings(self):
#         """An alias for `self.application.settings <Application.settings>`."""
#         return self.application.settings

#     def head(self, *args, **kwargs):
#         raise HTTPError(405)

#     def get(self, *args, **kwargs):
#         raise HTTPError(405)

#     def post(self, *args, **kwargs):
#         raise HTTPError(405)

#     def delete(self, *args, **kwargs):
#         raise HTTPError(405)

#     def patch(self, *args, **kwargs):
#         raise HTTPError(405)

#     def put(self, *args, **kwargs):
#         raise HTTPError(405)

#     def options(self, *args, **kwargs):
#         raise HTTPError(405)
