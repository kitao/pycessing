import os
import sys
import shutil
import urllib2
import zipfile

import settings


def setup():
    check_file = os.path.join(settings.COMMAND_AUX, '.setup_complete')

    if os.path.exists(check_file):
        check_mtime = os.stat(check_file).st_mtime
        settings_file = os.path.join(settings.COMMAND_PACKAGE, 'settings.py')
        command_mtime = os.stat(settings_file).st_mtime
        if check_mtime > command_mtime:
            return

    shutil.rmtree(settings.COMMAND_AUX, True)

    jython_dir = os.path.join(settings.COMMAND_LIB, 'jython')
    jython_filename = download_file(settings.JYTHON_URL, jython_dir)
    os.rename(jython_filename,
              os.path.join(settings.COMMAND_LIB, 'jython.jar'))
    shutil.rmtree(jython_dir, True)

    processing_dir = os.path.join(settings.COMMAND_LIB, 'processing')
    processing_filename = download_file(settings.PROCESSING_URL,
                                        processing_dir)
    unzip_file(processing_filename)

    processing_core_dir = os.path.join(processing_dir,
                                       settings.PROCESSING_CORE)
    shutil.copytree(processing_core_dir,
                    os.path.join(settings.COMMAND_LIB, 'core'))

    processing_ext_dir = os.path.join(processing_dir, settings.PROCESSING_LIBS)
    for name in os.listdir(processing_ext_dir):
        src_dir = os.path.join(processing_ext_dir, name)
        if os.path.isdir(src_dir):
            dest_dir = os.path.join(settings.COMMAND_LIB, name)
            shutil.copytree(src_dir, dest_dir)

    shutil.rmtree(processing_dir, True)

    examples_src_dir = os.path.join(settings.COMMAND_ROOT, 'examples')
    examples_dest_dir = os.path.join(settings.COMMAND_AUX, 'examples')
    print 'copy examples to {0}'.format(examples_dest_dir)
    shutil.copytree(examples_src_dir, examples_dest_dir)

    open(check_file, 'a').close()


def download_file(url, dest_dir):
    basename = os.path.basename(url)
    sys.stdout.write('download {0} ... '.format(basename))
    sys.stdout.flush()

    filename = os.path.join(dest_dir, basename)
    ensure_dir(dest_dir)

    with open(filename, 'wb') as f:
        f.write(urllib2.urlopen(url).read())

    print 'done'
    return filename


def unzip_file(filename):
    dest_dir, basename = os.path.split(filename)
    sys.stdout.write('unzip {0} ... '.format(basename))
    sys.stdout.flush()

    with zipfile.ZipFile(filename, 'r') as zf:
        zf.extractall(dest_dir)

    os.remove(filename)
    for root, dirs, files in os.walk(dest_dir):
        for name in files:
            if name.startswith('._'):
                os.remove(os.path.join(root, name))

    print 'done'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
