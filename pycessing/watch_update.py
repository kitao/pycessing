import time
import datetime
import os
import fnmatch
import stat


def get_current_time():
  return time.mktime(datetime.datetime.now().utctimetuple())


def get_latest_mtime(root_dir, file_pattern):
  latest_mtime = 0

  for root, dirs, files in os.walk(root_dir):
    for basename in files:
      if fnmatch.fnmatch(basename, file_pattern):
        filename = os.path.join(root, basename)
        latest_mtime = max(os.stat(filename)[stat.ST_MTIME], latest_mtime)

  return latest_mtime


def watch_update(root_dir, file_pattern, base_time, watch_interval):
  if get_latest_mtime(root_dir, file_pattern) > base_time:
    return False
  else:
    time.sleep(watch_interval)
    return True
