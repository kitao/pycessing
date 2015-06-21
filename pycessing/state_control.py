import sys


def get_state_info():
  state_info = {}
  state_info['modules'] = sys.modules.keys()
  return state_info


def restore_state(state_info):
  initial_modules = state_info['modules']
  for module in sys.modules.keys():
    if module not in initial_modules:
      del sys.modules[module]
      del module
