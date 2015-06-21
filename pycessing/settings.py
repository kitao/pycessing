import os
import sys

COMMAND_ROOT = os.path.abspath(os.path.dirname(__file__))
COMMAND_NAME = os.path.basename(COMMAND_ROOT)
COMMAND_AUX = os.path.join(os.path.expanduser('~'), '.' + COMMAND_NAME)
COMMAND_LIB = os.path.join(COMMAND_AUX, 'lib')

PROJECT_ROOT = os.path.abspath(os.path.join(COMMAND_ROOT, '..'))

PLATFORM = ('Mac' if sys.platform == 'darwin' else
            'Windows' if sys.platform == 'win32' else 'Linux')

JYTHON_URL = ('http://search.maven.org/remotecontent?filepath=org/python/'
              'jython-standalone/2.7.0/jython-standalone-2.7.0.jar')

PROCESSING_URL = {'Mac': 'http://download.processing.org/processing-2.2.1-macosx.zip',
                  'Windows': 'http://download.processing.org/processing-2.2.1-windows32.zip',
                  'Linux': 'http://download.processing.org/processing-2.2.1-linux32.tgz'}[PLATFORM]

PROCESSING_CORE = {'Mac': 'Processing.app/Contents/Java/core',
                   'Windows': 'processing-2.2.1/core',
                   'Linux': 'processing-2.2.1/core'}[PLATFORM]

PROCESSING_LIBS = {'Mac': 'Processing.app/Contents/Java/modes/java/libraries',
                   'Windows': 'processing-2.2.1/modes/java/libraries',
                   'Linux': 'processing-2.2.1/modes/java/libraries'}[PLATFORM]

WATCH_INTERVAL = 0.1
