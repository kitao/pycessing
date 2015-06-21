import sketch_info
from processing.core import PApplet


class App(PApplet):
  _instances = []

  def __init__(self, title=None, topmost=None, pos=None):
    App._instances.append(self)
    PApplet.__init__(self)

    self._title = title or sketch_info.basename
    self._topmost = topmost
    self._pos = pos
    print self._title, self._topmost, self._pos

  @classmethod
  def _update_apps(cls):
    print 'in update'
    for app in cls._instances:
      print 'in loop'
      if app._topmost:
        app.frame.setAlwaysOnTop(True)

        if app.frame.isAlwaysOnTop():
          app._topmost = None

      if app._pos:
        print 'pos 1'
        pos = app.frame.getLocation()
        app.frame.setLocation(app._pos[0], app._pos[1])
        print 'pos 2'

        if app._pos[0] == pos.x and app._pos[1] == pos.y:
          app._pos = None
          print 'pos 3'

  @classmethod
  def _dispose_apps(cls):
    for app in cls._instances:
      app.frame.dispose()
      app.dispose()

    cls._instances = []
    # del cls._instances[:]


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
