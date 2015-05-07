"""
scarlett.bootstrap
------------------------
Provides methods to bootstrap a ScarlettSystem instance.

"""

from scarlett.core.config import Config, ScarlettConfigLocations
import datetime
import os
import platform
import logging
import logging.config
import scarlett.errors
import pkgutil
import importlib
import sys

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

REGISTERED_FEATURES = []

_FEATURE_CACHE = {}

READY = False

# insert path so we can access things w/o having to re-install everything
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

scarlett.set_stream_logger('scarlett')

def ready(ss,feature_name=None):
    """ Prepares the loading of features. """
    global READY

    # Load the built-in features
    import scarlett.features as features

    del REGISTERED_FEATURES[:]

    if feature_name == None:

       REGISTERED_FEATURES.extend(
           item[1] for item in
           pkgutil.iter_modules(features.__path__, 'scarlett.features.'))

    else:

       REGISTERED_FEATURES.append(feature_name)

    READY = True

def set_feature(feature_name, feature):
    """ Sets a feature in the cache. """
    _check_ready()

    _FEATURE_CACHE[feature_name] = feature

def setup_feature(ss, scarlett_feature):
    """ Setup a feature for Scarlett. """
    # Check if already loaded
    if scarlett_feature in ss.features:
        scarlett.log.info(Fore.YELLOW + "feature %s failed to initialize", scarlett_feature)
        return

    _ensure_scarlett_ready(ss)

    feature = get_feature(scarlett_feature)

    try:
        # setup a scarlett feature
        if feature.setup_feature(ss):
            ss.features.append(feature.SCARLETT_FEATURE)

            scarlett.log.info(Fore.YELLOW + "feature %s initialized", scarlett_feature)

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(ss.features)

            # if group.SCARLETT_FEATURE not in feature.DEPENDENCIES:
            #     ss.pool.add_worker()

            # TODO: this might be the perfect area to do a worker creation and
            # to do a gobject.GObject.connect

            return True

        else:
            scarlett.log.error(Fore.RED + "feature %s failed to initialize", scarlett_feature)

    except Exception:
        scarlett.log.exception(Fore.RED + "Error during setup of feature %s", scarlett_feature)

    return False

def connect_to_scarlett(ss, scarlett_feature):
    pass

def get_feature(feature_name):
    """ Tries to load specified feature.
        Looks in config dir first, then built-in features.
        Only returns it if also found to be valid. """

    if feature_name in _FEATURE_CACHE:
        return _FEATURE_CACHE[feature_name]

    _check_ready()

    # TODO: Add base features here as well including voice, scarlettbrain, etc
    potential_paths = ['scarlett.features.{}'.format(feature_name)]

    for path in potential_paths:
        # Validate here that root feature exists
        # If path contains a '.' we are specifying a sub-feature
        # Using rsplit we get the parent feature from sub-feature
        root_comp = path.rsplit(".", 1)[0] if '.' in feature_name else path
        scarlett.log.info(Fore.GREEN + "root_comp: %s" % root_comp)

        # if root_comp not in AVAILABLE_features:
        #     continue

        try:
            module = importlib.import_module(path)

            scarlett.log.info(Fore.GREEN + "Loaded %s from %s" % (feature_name, path))

            _FEATURE_CACHE[feature_name] = module

            return module

        except ImportError:
            scarlett.log.debug(
                Fore.RED + "Error loading %s. Make sure all "
                 "dependencies are installed" % path)

    scarlett.log.debug(Fore.RED + "Unable to find feature %s" % feature_name)

    return None

# DISABLED # def _setup_features(ss):
# DISABLED #
# DISABLED #     del REGISTERED_FEATURES[:]
# DISABLED #
# DISABLED #     #_feat_enable_config = scarlett.config.get('features','enable')
# DISABLED #
# DISABLED #     #_features_to_register = tuple(_feat_enable_config.split(','))
# DISABLED #
# DISABLED #     # REGISTERED_FEATURES.extend(
# DISABLED #     #     item[1] for item in
# DISABLED #     #     pkgutil.iter_modules(features.__path__, 'scarlett.features.'))
# DISABLED #
# DISABLED #     REGISTERED_FEATURES.append('time')
# DISABLED #
# DISABLED #     feature_name = REGISTERED_FEATURES[0]
# DISABLED #
# DISABLED #     # First check custom, then built-in
# DISABLED #     potential_paths = ['scarlett.features.{}'.format(REGISTERED_FEATURES[0])]
# DISABLED #
# DISABLED #     for path in potential_paths:
# DISABLED #         # Validate here that root feature exists
# DISABLED #         # If path contains a '.' we are specifying a sub-feature
# DISABLED #         # Using rsplit we get the parent feature from sub-feature
# DISABLED #         root_comp = path.rsplit(".", 1)[0] if '.' in feature_name else path
# DISABLED #
# DISABLED #         # if root_comp not in REGISTERED_FEATURES:
# DISABLED #         #    continue
# DISABLED #
# DISABLED #         try:
# DISABLED #             module = importlib.import_module(path)
# DISABLED #
# DISABLED #             scarlett.log.info(Fore.GREEN + "Loaded %s from %s", feature_name, path)
# DISABLED #
# DISABLED #             _FEATURE_CACHE[feature_name] = module
# DISABLED #
# DISABLED #             return module
# DISABLED #
# DISABLED #         except ImportError:
# DISABLED #             scarlett.log.debug(
# DISABLED #                 Fore.RED + "Error loading %s. Make sure all "
# DISABLED #                  "dependencies are installed" % path)
# DISABLED #             scarlett.log.debug(Fore.RED + "Unable to find feature %s" % feature_name)
# DISABLED #
# DISABLED #     return None

def system_boot(ss=None):
    """ initalize a new instance of ScarlettSystem if it doesnt already
    exist.
    """
    if ss is None:
       ss = scarlett.ScarlettSystem()

    _ensure_scarlett_ready(ss)

    _feat_enable_config = scarlett.config.get('features','enable')

    _features_to_register = tuple(_feat_enable_config.split(','))

    # eliminate anything that isn't a string
    _features_to_register = [x for x in _features_to_register if isinstance(x, basestring)]

    for scarlett_feature in _features_to_register(_features_to_register):
        setup_feature(ss, scarlett_feature)

    return ss

def _check_ready():
    """ Issues a warning if bootstrap.prepare() has never been called. """
    if not READY:
        scarlett.log.debug(
                Fore.RED + "You did not call bootstrap.ready() yet. " +
                "Certain functionality might not be working."
                )

def _ensure_scarlett_ready(ss):
    """ Ensure Scarlett is ready dependencies are ready. """
    if not READY:
        ready(ss)
