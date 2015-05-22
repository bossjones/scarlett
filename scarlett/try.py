#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import pkgutil
import sys
import os
import importlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import scarlett

CORE_MODULES = {
  'brain':{
    'module_path':'scarlett.brain.',
    'module_name':'scarlettbrainfsm'
   },
  'player':{
    'module_path':'scarlett.basics.',
    'module_name':'say'
  },
  'speaker':{
    'module_path':'scarlett.basics.',
    'module_name':'voice'
  },
  'listener':{
    'module_path':'scarlett.listener.',
    'module_name':'gstlisteneri'
  }
}

# scarlett.brain.scarlettbrainfsm.scarlettbraini
feature_name = 'brain'
folder_name = CORE_MODULES[feature_name]['module_path'].split('.')[1]
module_name = CORE_MODULES[feature_name]['module_name']

module_paths = '{}'.format(CORE_MODULES[feature_name]['module_path'])
potential_paths = 'scarlett.{}.{}'.format(folder_name,module_name)

if feature_name ==  'brain':
   # modules = pkgutil.iter_modules(path)
   modules = pkgutil.iter_modules(scarlett.brain.__path__, CORE_MODULES[feature_name]['module_path'])

for module_loader, mod_name, ispkg in modules:

    if mod_name not in sys.modules and mod_name == potential_paths:

            print "potential_paths: " + potential_paths + "\n"
            print "modules: "
            print modules
            print "\n"

            print "mod_name: \n"
            print mod_name
            print "\n"

            print mod_name == potential_paths
            print mod_name
            print potential_paths
            try:
              # Import module
              # eg: scarlett.brain.scarlettbrainfsm
              loaded_mod = importlib.import_module(potential_paths)

              # Load class from imported module
              # eg: ScarlettBrainFSM
              class_name = loaded_mod
              print class_name

              loaded_class = getattr(loaded_mod, 'setup_core')(None)

              # Create an instance of the class
              instance = loaded_class
              print instance
              instance.hello()

            except ImportError:
              print 'helllloooooooo'
