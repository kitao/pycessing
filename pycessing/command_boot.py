import os
import sys
import subprocess

import settings


def boot():
  java_opts = '-Dpython.cachedir.skip=false'
  jython_file = os.path.join(settings.COMMAND_LIB, 'jython.jar')
  runner_file = os.path.join(settings.COMMAND_ROOT, 'sketch_runner.py')
  command_args = ' '.join(sys.argv[1:])

  subprocess.call('java {0} -jar {1} {2} {3}'.format(
      java_opts, jython_file, runner_file, command_args), shell=True)
