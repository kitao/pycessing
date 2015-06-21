import os

filename = None
dirname = None
basename = None
modname = None


def init_sketch_info(sketchfile):
  global filename, dirname, basename, modname
  filename = os.path.abspath(sketchfile)
  dirname = os.path.dirname(filename)
  basename = os.path.basename(filename)
  modname = os.path.splitext(basename)[0]
