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
    for dirname in os.listdir(processing_ext_dir):
        src_dir = os.path.join(processing_ext_dir, dirname)
        if os.path.isdir(src_dir):
            dest_dir = os.path.join(settings.COMMAND_LIB, dirname)
            shutil.copytree(src_dir, dest_dir)

    shutil.rmtree(processing_dir, True)

    examples_src_dir = os.path.join(settings.COMMAND_ROOT, 'examples')
    examples_dest_dir = os.path.join(settings.COMMAND_AUX, 'examples')
    print 'copy examples to {0}'.format(examples_dest_dir)
    shutil.copytree(examples_src_dir, examples_dest_dir)

    open(check_file, 'a').close()


def download_file(url, output_dir):
    basename = os.path.basename(url)
    sys.stdout.write('download {0} ... '.format(basename))
    sys.stdout.flush()

    filename = os.path.join(output_dir, basename)
    ensure_dir(output_dir)

    with open(filename, 'wb') as f:
        f.write(urllib2.urlopen(url).read())

    print 'done'
    return filename


def unzip_file(zip_filename):
    output_dir, basename = os.path.split(zip_filename)
    sys.stdout.write('unzip {0} ... '.format(basename))
    sys.stdout.flush()

    zf = zipfile.ZipFile(zip_filename, 'r')
    zf.extractall(output_dir)
    zf.close()

    os.remove(zip_filename)
    print 'done'


def ensure_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)
