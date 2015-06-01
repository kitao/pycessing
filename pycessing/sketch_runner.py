import os
import sys

import settings
import system_vars


def load_library(name):
    lib_dir = os.path.join(settings.COMMAND_LIB, name, 'library')
    if load_all_jars(lib_dir):
        return True
    else:
        print 'library not found -- {0}'.format(name)
        return False


def load_all_jars(path):
    import fnmatch

    if not os.path.isdir(path):
        return False

    is_success = False
    for name in os.listdir(path):
        if fnmatch.fnmatch(name, '*.jar'):
            # sys.path.append(os.path.join(path, name))
            load_jar(os.path.join(path, name))
            is_success = True
            print 'jar file added -- {0}'.format(name)
    return is_success


def load_jar(jar_file):
    import java.io
    import java.net
    import java.lang

    url = (java.io.File(jar_file).toURL()
           if type(jar_file) != java.net.URL else jar_file)
    method = java.net.URLClassLoader.getDeclaredMethod('addURL',
                                                       [java.net.URL])
    method.accessible = 1
    method.invoke(java.lang.ClassLoader.getSystemClassLoader(), [url])

    # from java.util.jar import JarFile
    # jf = JarFile(jar_file)
    # for e in jf.entries():
    #     print e


def complete_path(path):
    return os.path.join(system_vars.sketch_dir, path)


def start(sketch, title=None, topmost=False, pos=None):
    if not title:
        title = system_vars.sketch_name

    from processing.core import PApplet
    PApplet.runSketch([title], sketch)

    if topmost:
        system_vars.system_requests.append(
            {'command': 'topmost', 'sketch': sketch})

    if pos:
        system_vars.system_requests.append(
            {'command': 'pos', 'sketch': sketch, 'pos': pos})


def reload2():
    system_vars.system_requests.append({'command': 'reload'})


def create_frame():
    import java.awt.event
    import java.awt
    import javax.swing

    class KL(java.awt.event.KeyListener):
        def keyPressed(self, e):
            print '*****'
            print e
            exit()

    frame = javax.swing.JFrame()
    frame.setUndecorated(True)
    frame.getRootPane().setWindowDecorationStyle(javax.swing.JRootPane.FRAME)
    frame.addKeyListener(KL())
    frame.setVisible(True)


is_exit = False


def run_sketch():
    print 'start'
    create_frame()

    if len(sys.argv) < 2:
        print 'usage: {0} [sketchfile]'.format(settings.COMMAND_NAME)
        sys.exit()

    system_vars.sketch_file = os.path.abspath(sys.argv[1])
    system_vars.sketch_name = os.path.splitext(
        os.path.basename(system_vars.sketch_file))[0]
    system_vars.sketch_dir = os.path.dirname(system_vars.sketch_file)

    if not os.path.exists(system_vars.sketch_file):
        print 'sketch file not found -- {0}'.format(system_vars.sketch_file)
        sys.exit()

    if not load_library('core'):
        sys.exit()

    from processing.core import PApplet  # NOQA

    sys.path.append(settings.COMMAND_ROOT)
    sys.path.insert(0, system_vars.sketch_dir)

    initial_modules = sys.modules.copy()

    import threading
    import getch

    def check_exit():
        while True:
            key = ord(getch.getch())
            if key == 27:
                global is_exit
                is_exit = True

    threading.Thread(target=check_exit).start()

    while True:
        # run sketh
        print '\n****** START SKETCH ******\n'

        try:
            __import__(system_vars.sketch_name)
        except Exception as e:
            print e

        # watch file changed
        # TBD
        while True:
            import time
            time.sleep(0.1)
            if is_exit:
                exit()

        # restore execution environment
        for sketch in system_vars.sketch_instances:
            sketch.frame.dispose()
            sketch.dispose()

        del system_vars.sketch_instances[:]
        system_vars.system_requests.clear()

        sys.modules = initial_modules  # TODO

        import java.lang
        java.lang.System.gc()

'''
  INITIAL_FEATURES = $LOADED_FEATURES.dup
  INITIAL_CONSTANTS = Object.constants - [:INITIAL_CONSTANTS]

  loop do
    # run sketch
    print "\n****** START SKETCH ******\n\n"

    Thread.new do
      begin
        Object::TOPLEVEL_BINDING.eval(File.read(sketch_file), sketch_file)
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

        Find.find(sketch_dir) do |file|
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


if __name__ == '__main__':
    run_sketch()
