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

       AVAILABLE_features.extend(
           item[1] for item in
           pkgutil.iter_modules(features.__path__, 'scarlett.features.'))

    else:

       REGISTERED_FEATURES.append(feature_name)

    READY = True

def set_feature(feature_name, feature):
    """ Sets a feature in the cache. """
    _check_ready()

    _FEATURE_CACHE[feature_name] = feature

def setup_feature(ss, scarlett_feature, config=None):
    """ Setup a feature for Scarlett. """
    # Check if already loaded
    if scarlett_feature in ss.features:
        return

    _ensure_loader_prepared(hass)

    if config is None:
        config = defaultdict(dict)

    feature = get_feature(scarlett_feature)

    try:
        if feature.setup(ss):
            hass.features.append(feature.DOMAIN)

            _LOGGER.info("feature %s initialized", scarlett_feature)

            # Assumption: if a feature does not depend on groups
            # it communicates with devices
            if group.DOMAIN not in feature.DEPENDENCIES:
                hass.pool.add_worker()

            return True

        else:
            _LOGGER.error("feature %s failed to initialize", scarlett_feature)

    except Exception:  # pylint: disable=broad-except
        _LOGGER.exception("Error during setup of feature %s", scarlett_feature)

    return False

def get_feature(feature_name):
    """ Tries to load specified feature.
        Looks in config dir first, then built-in features.
        Only returns it if also found to be valid. """

    if feature_name in _FEATURE_CACHE:
        return _FEATURE_CACHE[feature_name]

    _check_ready()

    potential_paths = ['scarlett.features.{}'.format(feature_name)]

    for path in potential_paths:
        # Validate here that root feature exists
        # If path contains a '.' we are specifying a sub-feature
        # Using rsplit we get the parent feature from sub-feature
        root_comp = path.rsplit(".", 1)[0] if '.' in feature_name else path

        # if root_comp not in AVAILABLE_features:
        #     continue

        try:
            module = importlib.import_module(path)

            scarlett.log.info(Fore.GREEN + "Loaded %s from %s", feature_name, path)

            _FEATURE_CACHE[feature_name] = module

            return module

        except ImportError:
            scarlett.log.debug(
                Fore.RED + "Error loading %s. Make sure all "
                 "dependencies are installed" % path)

    scarlett.log.debug(Fore.RED + "Unable to find feature %s" % feature_name)

    return None


def _setup_features(ss):

    del REGISTERED_FEATURES[:]

    #_feat_enable_config = scarlett.config.get('features','enable')

    #_features_to_register = tuple(_feat_enable_config.split(','))

    # REGISTERED_FEATURES.extend(
    #     item[1] for item in
    #     pkgutil.iter_modules(features.__path__, 'scarlett.features.'))

    REGISTERED_FEATURES.append('time')

    feature_name = REGISTERED_FEATURES[0]

    # First check custom, then built-in
    potential_paths = ['scarlett.features.{}'.format(REGISTERED_FEATURES[0])]

    for path in potential_paths:
        # Validate here that root feature exists
        # If path contains a '.' we are specifying a sub-feature
        # Using rsplit we get the parent feature from sub-feature
        root_comp = path.rsplit(".", 1)[0] if '.' in feature_name else path

        # if root_comp not in REGISTERED_FEATURES:
        #    continue

        try:
            module = importlib.import_module(path)

            scarlett.log.info(Fore.GREEN + "Loaded %s from %s", feature_name, path)

            _FEATURE_CACHE[feature_name] = module

            return module

        except ImportError:
            scarlett.log.debug(
                Fore.RED + "Error loading %s. Make sure all "
                 "dependencies are installed" % path)
            scarlett.log.debug(Fore.RED + "Unable to find feature %s" % feature_name)

    return None

# def setup_feature(hass, domain, config=None):
#     """ Setup a feature for Home Assistant. """
#     # Check if already loaded
#     if domain in hass.features:
#         return

#     _ensure_loader_ready(hass)

#     if config is None:
#         config = defaultdict(dict)

#     feature = loader.get_feature(domain)

#     try:
#         if feature.setup(hass, config):
#             hass.features.append(feature.DOMAIN)

#             _LOGGER.info("feature %s initialized", domain)

#             # Assumption: if a feature does not depend on groups
#             # it communicates with devices
#             if group.DOMAIN not in feature.DEPENDENCIES:
#                 hass.pool.add_worker()

#             return True

#         else:
#             _LOGGER.error("feature %s failed to initialize", domain)

#     except Exception:  # pylint: disable=broad-except
#         _LOGGER.exception("Error during setup of feature %s", domain)

#     return False

def system_boot(ss=None):
    """ initalize a new instance of ScarlettSystem if it doesnt already
    exist.
    """
    if ss is None:
       ss = scarlett.ScarlettSystem()

    _ensure_scarlett_ready(ss)

    # Filter out the repeating and common config section [homeassistant]
    features = (key for key in config.keys()
                  if ' ' not in key and key != homeassistant.DOMAIN)

    _feat_enable_config = scarlett.config.get('features','enable')

    _features_to_register = tuple(_feat_enable_config.split(','))

    for scarlett_feature in _features_to_register(_features_to_register):
        setup_feature(ss, scarlett_feature)

    #_setup_features(ss)

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
