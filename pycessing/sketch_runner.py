import os
import sys

import settings
import sketch_info

import state_control
import watch_update

import gui


def load_library(name):
  lib_dir = os.path.join(settings.COMMAND_LIB, name, 'library')
  if load_all_jars(lib_dir):
    return True
  else:
    print 'library not found -- {0}'.format(name)
    return False


def load_all_jars(path):
  import fnmatch

  if not os.path.isdir(path):
    return False

  is_success = False
  for name in os.listdir(path):
    if fnmatch.fnmatch(name, '*.jar'):
      # sys.path.append(os.path.join(path, name))
      load_jar(os.path.join(path, name))
      is_success = True
      print 'jar file added -- {0}'.format(name)
    return is_success


def load_jar(jar_file):
  import java.io
  import java.net
  import java.lang

  url = (java.io.File(jar_file).toURL()
         if type(jar_file) != java.net.URL else jar_file)
  method = java.net.URLClassLoader.getDeclaredMethod('addURL',
                                                     [java.net.URL])
  method.accessible = 1
  method.invoke(java.lang.ClassLoader.getSystemClassLoader(), [url])

  # from java.util.jar import JarFile
  # jf = JarFile(jar_file)
  # for e in jf.entries():
  #     print e


def complete_path(path):
  return os.path.join(sketch_info.sketch_dir, path)


def run_app(app):
  from processing.core import PApplet
  PApplet.runSketch([app._title], app)


_to_reload = False
_to_exit = False


def reload_sketch():
  global _to_reload
  _to_reload = True


def exit_sketch():
  global _to_exit
  _to_exit = True


def start():
  if len(sys.argv) < 2:
    print 'usage: {0} [sketchfile]'.format(settings.COMMAND_NAME)
    sys.exit()

  sketch_info.init_sketch_info(sys.argv[1])

  if not os.path.exists(sketch_info.filename):
    print 'sketch file not found -- {0}'.format(sketch_info.filename)
    sys.exit()

  if not load_library('core'):
    sys.exit()

  from processing.core import PApplet  # NOQA

  sys.path.append(settings.COMMAND_ROOT)
  sys.path.insert(0, sketch_info.dirname)

  state_info = state_control.get_state_info()

  gui.create(reload_sketch, exit_sketch)

  import app

  while True:
    # run sketh
    print '\n****** START SKETCH ******\n'

    try:
      __import__(sketch_info.modname)
    except Exception as e:
      print e

    # watch file changed
    base_time = watch_update.get_current_time()
    while watch_update.watch_update(
        sketch_info.dirname, '*.py', base_time, settings.WATCH_INTERVAL):
      app.App._update_apps()

      global _to_reload, _to_exit

      if _to_reload:
        _to_reload = False
        break

      if _to_exit:
        exit()

    # restore execution environment
    app.App._dispose_apps()

    state_control.restore_state(state_info)

    import java.lang
    java.lang.System.gc()


if __name__ == '__main__':
  start()
