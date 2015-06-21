import os
import shutil

import settings
import download


def setup():
  check_file = os.path.join(settings.COMMAND_AUX, '.setup_complete')

  if os.path.exists(check_file):
    check_mtime = os.stat(check_file).st_mtime

    settings_file = os.path.join(settings.COMMAND_ROOT, 'settings.py')
    command_mtime = os.stat(settings_file).st_mtime

    if check_mtime > command_mtime:
      return

  shutil.rmtree(settings.COMMAND_AUX, True)

  # download Jython
  jython_dir = os.path.join(settings.COMMAND_LIB, 'jython')
  jython_filename = download.download(settings.JYTHON_URL, jython_dir)
  os.rename(jython_filename, os.path.join(settings.COMMAND_LIB, 'jython.jar'))
  shutil.rmtree(jython_dir, True)

  # download and unzip Processing
  processing_dir = os.path.join(settings.COMMAND_LIB, 'processing')
  processing_filename = download.download(settings.PROCESSING_URL, processing_dir)
  download.unzip(processing_filename)

  processing_core_dir = os.path.join(processing_dir, settings.PROCESSING_CORE)
  shutil.copytree(processing_core_dir, os.path.join(settings.COMMAND_LIB, 'core'))

  processing_ext_dir = os.path.join(processing_dir, settings.PROCESSING_LIBS)
  for name in os.listdir(processing_ext_dir):
    src_dir = os.path.join(processing_ext_dir, name)
    if os.path.isdir(src_dir):
      dest_dir = os.path.join(settings.COMMAND_LIB, name)
      shutil.copytree(src_dir, dest_dir)

  shutil.rmtree(processing_dir, True)

  # copy examples
  examples_src_dir = os.path.join(settings.PROJECT_ROOT, 'examples')
  examples_dest_dir = os.path.join(settings.COMMAND_AUX, 'examples')
  print 'copy examples to {0}'.format(examples_dest_dir)
  shutil.copytree(examples_src_dir, examples_dest_dir)

  open(check_file, 'a').close()
