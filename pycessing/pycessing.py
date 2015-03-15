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


class SketchBase:
    pass
'''
  # The base class of a Processing sketch
  class SketchBase < PApplet
    %w(
      displayHeight displayWidth frameCount keyCode
      mouseButton mouseX mouseY pmouseX pmouseY
    ).each do |name|
      sc_name = name.split(/(?![a-z])(?=[A-Z])/).map(&:downcase).join('_')
      alias_method sc_name, name
    end

    def self.method_added(name)
      name = name.to_s
      if name.include?('_')
        lcc_name = name.split('_').map(&:capitalize).join('')
        lcc_name[0] = lcc_name[0].downcase
        alias_method lcc_name, name if lcc_name != name
      end
    end

    def method_missing(name, *args)
      self.class.__send__(name, *args) if PApplet.public_methods.include?(name)
    end

    def get_field_value(name)
      java_class.declared_field(name).value(to_java(PApplet))
    end

    def initialize
      super
      SKETCH_INSTANCES << self
    end

    def frame_rate(fps = nil)
      return get_field_value('frameRate') unless fps
      super(fps)
    end

    def key
      code = get_field_value('key')
      code < 256 ? code.chr : code
    end

    def key_pressed?
      get_field_value('keyPressed')
    end

    def mouse_pressed?
      get_field_value('mousePressed')
    end
  end
'''
