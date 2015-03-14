import os
import sys
import subprocess

import settings


def start():
    jython_file = os.path.join(settings.COMMAND_LIB, 'jython.jar')
    runner_file = os.path.join(settings.COMMAND_PACKAGE, 'sketch_runner.py')
    command_args = ' '.join(sys.argv[1:])

    subprocess.call('java -jar {0} {1} {2}'.format(
        jython_file, runner_file, command_args), shell=True)
