import os
import sys
import fnmatch

import settings


def load_library(name):
    lib_dir = os.path.join(settings.COMMAND_LIB, name, 'library')
    if add_jars(lib_dir):
        return True
    else:
        print 'library not found -- {0}'.format(name)
        return False


def add_jars(path):
    if not os.path.isdir(path):
        return False

    is_success = False
    for name in os.listdir(path):
        if fnmatch.fnmatch(name, '*.jar'):
            sys.path.append(os.path.join(path, name))
            is_success = True
            print 'jar file added -- {0}'.format(name)
    return is_success


def import_package(package):
    pass

'''
  def self.import_package(package, module_name)
    code = "module #{module_name}; include_package '#{package}'; end"
    Object::TOPLEVEL_BINDING.eval(code)
  end
'''


def complete_path(path):
    return os.path.join(sketch_runner.sketch_dir, path)


def start(sketch, title=None, topmost=False, pos=None):
    '''
    title = opts[:title] || SKETCH_NAME
    topmost = opts[:topmost]
    pos = opts[:pos]

    PApplet.run_sketch([title], sketch)
    '''

    if topmost:
        sketch_runner.system_requests.append(
            {'command': 'topmost', 'sketch': sketch})

    if pos:
        sketch_runner.system_requests.append(
            {'command': 'pos', 'sketch': sketch, 'pos': pos})


def reload():
    sketch_runner.system_requests.append({'command': 'reload'})


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'usage: {0} [sketchfile]'.format(settings.COMMAND_NAME)
        sys.exit()

    sketch_file = os.path.abspath(sys.argv[1])
    sketch_name = os.path.splitext(os.path.basename(sketch_file))[0]
    sketch_dir = os.path.dirname(sketch_file)

    system_requests = []
    sketch_instances = []

    if not os.path.exists(sketch_file):
        print 'sketch file not found -- {0}'.format(sketch_file)
        sys.exit()

    if not load_library('core'):
        sys.exit()

    from processing.core import *  # NOQA
    from processing.opengl import *  # NOQA

    sys.path.append(settings.COMMAND_ROOT)

    # sys.path.insert(0, sketch_dir)
    # __import__(sketch_name)
    execfile(sketch_file)

'''
  INITIAL_FEATURES = $LOADED_FEATURES.dup
  INITIAL_CONSTANTS = Object.constants - [:INITIAL_CONSTANTS]

  loop do
    # run sketch
    print "\n****** START SKETCH ******\n\n"

    Thread.new do
      begin
        Object::TOPLEVEL_BINDING.eval(File.read(SKETCH_FILE), SKETCH_FILE)
      rescue Exception => e
        puts e
      end
    end

    # watch file changed
    execute_time = Time.now

    catch :break_loop do
      loop do
        SYSTEM_REQUESTS.each do |request|
          case request[:command]
          when :topmost
            sketch = request[:sketch]
            sketch.frame.set_always_on_top(true)

            is_always_on_top = sketch.frame.is_always_on_top
            SYSTEM_REQUESTS.delete(request) if is_always_on_top
          when :pos
            sketch = request[:sketch]
            pos_x, pos_y = request[:pos]
            sketch.frame.set_location(pos_x, pos_y)

            cur_pos = sketch.frame.get_location
            is_pos_set = cur_pos.x == pos_x && cur_pos.y == pos_y
            SYSTEM_REQUESTS.delete(request) if is_pos_set
          when :reload
            throw :break_loop
          end
        end

        Find.find(SKETCH_DIR) do |file|
          is_ruby = FileTest.file?(file) && File.extname(file) == '.rb'
          throw :break_loop if is_ruby && File.mtime(file) > execute_time
        end

        sleep(WATCH_INTERVAL)
      end
    end

    # restore execution environment
    SKETCH_INSTANCES.each do |sketch|
      sketch.frame.dispose
      sketch.dispose
    end

    SKETCH_INSTANCES.clear
    SYSTEM_REQUESTS.clear

    added_constants = Object.constants - INITIAL_CONSTANTS
    added_constants.each do |constant|
      Object.class_eval { remove_const constant }
    end

    added_features = $LOADED_FEATURES - INITIAL_FEATURES
    added_features.each { |feature| $LOADED_FEATURES.delete(feature) }

    java.lang.System.gc
  end
'''
