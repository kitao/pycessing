import os
import sys
import urllib2


def download(url, dest_dir):
  basename = os.path.basename(url)
  sys.stdout.write('download {0} ... '.format(basename))
  sys.stdout.flush()

  filename = os.path.join(dest_dir, basename)

  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

  with open(filename, 'wb') as f:
    f.write(urllib2.urlopen(url).read())

    print 'done'
    return filename


def unzip(filename):
  import zipfile

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


def url_to_filename(url, dest_dir):
  basename = os.path.basename(url)


def makedirs(path):
  if not os.path.exists(path):
    os.makedirs(path)
