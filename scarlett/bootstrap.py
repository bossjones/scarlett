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
import pprint
import scarlett

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
    from scarlett.constants import *
    from scarlett import __version__
except:
    gobjectnotimported = True

# All scarlett feature objects that have been registered
REGISTERED_FEATURES = []

# All scarlett feature that have already been initalized and cached
_FEATURE_CACHE = {}

# Prereqs required to begin importing features
READY = False

# Scarlett core modules, required to get her up and running
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


def ready(ss, feature_name=None):
    """ Prepares the loading of features. """
    global READY

    # Load the built-in features
    import scarlett.features as features

    del REGISTERED_FEATURES[:]

    if feature_name is None:

        REGISTERED_FEATURES.extend(
            item[1] for item in
            pkgutil.iter_modules(features.__path__, 'scarlett.features.'))

    else:

        REGISTERED_FEATURES.append(feature_name)

    READY = True


def folder_name_to_str(core_feature_name):
    return CORE_MODULES[core_feature_name]['module_path'].split('.')[1]


def module_name_to_str(core_feature_name):
    return CORE_MODULES[core_feature_name]['module_name']


def module_path_to_str(core_feature_name):
    return '{}'.format(CORE_MODULES[core_feature_name]['module_path'])


def potential_path_to_str(core_feature_name):
    return 'scarlett.{}.{}'.format(
        folder_name_to_str(core_feature_name),
        module_name_to_str(core_feature_name)
    )


def setup_core_feature(ss, mod_name):
    """
    Setup core feature for Scarlett.
    Eg. Brain, Speaker, Player, Listener
    """
    global CORE_MODULES

    core_feature_name = mod_name
    scarlett.log.debug(
            Fore.RED + "core_feature_name {}.".format(core_feature_name))

    # folder_name = folder_name_to_str(core_feature_name)
    # module_name = module_name_to_str(core_feature_name)
    module_paths = module_path_to_str(core_feature_name)
    potential_paths = potential_path_to_str(core_feature_name)

    scarlett.log.debug(
            Fore.RED + "module_paths {}.".format(module_paths))
    scarlett.log.debug(
            Fore.RED + "potential_paths {}.".format(potential_paths))

    if core_feature_name == 'brain':
        modules = pkgutil.iter_modules(scarlett.brain.__path__, module_paths)
    elif core_feature_name == 'speaker':
        modules = pkgutil.iter_modules(scarlett.basics.__path__, module_paths)
    elif core_feature_name == 'player':
        modules = pkgutil.iter_modules(scarlett.basics.__path__, module_paths)
    elif core_feature_name == 'listener':
        modules = pkgutil.iter_modules(
            scarlett.listener.__path__, module_paths)
        scarlett.log.debug(
            Fore.RED + "modules {}.".format(modules))
    else:
        scarlett.log.debug(
            Fore.RED + "Error loading {}.".format(core_feature_name))
        return False

    for module_loader, mod_name, ispkg in modules:
        scarlett.log.debug(
            Fore.RED + "mod_name {}.".format(mod_name))
        scarlett.log.debug(
            Fore.RED + "module_loader {}.".format(module_loader))
        scarlett.log.debug(
            Fore.RED + "ispkg {}.".format(ispkg))

        if mod_name not in sys.modules and mod_name == potential_paths:
            try:
                # Import module
                # eg: scarlett.brain.scarlettbrainfsm
                loaded_mod = importlib.import_module(potential_paths)

                loaded_class = getattr(loaded_mod, 'setup_core')(ss)

                # Create an instance of the class
                instance = loaded_class
                instance.hello()

                # TODO: Add a connect function to the scarlett system
                # HERE

                return instance

            except ImportError:
                scarlett.log.debug(
                    Fore.RED + "Module load FAILED: {}".format(
                        potential_paths)
                )
            return False


def set_feature(feature_name, feature):
    """ Sets a feature in the cache. """
    _check_ready()

    _FEATURE_CACHE[feature_name] = feature


def setup_feature(ss, scarlett_feature):
    """ Setup a feature for Scarlett. """
    # Check if already loaded
    if scarlett_feature in ss.features:
        scarlett.log.info(
            Fore.YELLOW + "feature %s failed to initialize", scarlett_feature)
        return

    _ensure_scarlett_ready(ss)

    feature = get_feature(scarlett_feature)

    try:
        # setup a scarlett feature
        if feature.setup_feature(ss):
            ss.features.append(feature.SCARLETT_FEATURE)

            scarlett.log.info(
                Fore.YELLOW + "feature %s initialized", scarlett_feature)

            pp = pprint.PrettyPrinter(indent=4)
            pp.pprint(ss.features)

            # if group.SCARLETT_FEATURE not in feature.DEPENDENCIES:
            #     ss.pool.add_worker()

            connect_to_scarlett(ss, feature)

            return True

        else:
            scarlett.log.error(
                Fore.RED + "feature %s failed to initialize", scarlett_feature)

    except Exception:
        scarlett.log.exception(
            Fore.RED + "Error during setup of feature %s", scarlett_feature)

    return False


def connect_to_scarlett(ss, sf):
    sf._INSTANCE.connect(sf.CONNECT_NAME, ss.scarlett_event_cb)
    sf._INSTANCE.start()


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

            scarlett.log.info(
                Fore.GREEN + "Loaded %s from %s" % (feature_name, path))

            _FEATURE_CACHE[feature_name] = module

            return module

        except ImportError:
            scarlett.log.debug(
                Fore.RED + "Error loading %s. Make sure all "
                "dependencies are installed" % path)

    scarlett.log.debug(Fore.RED + "Unable to find feature %s" % feature_name)

    return None


def system_boot(ss=None):
    """ initalize a new instance of ScarlettSystem if it doesnt already
    exist.
    """
    if ss is None:
        ss = scarlett.ScarlettSystem()

    _ensure_scarlett_ready(ss)

    # Begin: Enable scarlett features

    _feat_enable_config = scarlett.config.get('features', 'enable')

    _features_to_register = tuple(_feat_enable_config.split(','))

    # eliminate anything that isn't a string
    _features_to_register = [
        x for x in _features_to_register if isinstance(x, basestring)]

    for scarlett_feature in _features_to_register:
        setup_feature(ss, scarlett_feature)

    # End: Enable scarlett features

    # TODO: set this to ('brain','listener')
    ### _core_features_to_register = ('speaker',)
    _core_features_to_register = ("brain",)

    _core_features_to_register = [
        x for x in _core_features_to_register if isinstance(x, basestring)]

    for scarlett_core in _core_features_to_register:
        setup_core_feature(ss, scarlett_core)

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
