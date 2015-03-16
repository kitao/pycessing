from javax.swing import JFrame
from processing.core import PApplet


class Sketch(PApplet):
    def __init__(self):
        PApplet.__init__(self)
        print '111'

    def setup(self):
        self.size(400, 300)
        print '222'

    def draw(self):
        self.background(128)
        print '333'


def run(applet):
    frame = JFrame(title="Processing camera",
                   resizable=1,
                   defaultCloseOperation=JFrame.EXIT_ON_CLOSE)
    frame.contentPane.add(applet)
    applet.init()
    frame.pack()
    frame.visible = 1

sketch = Sketch()
# run(sketch)
PApplet.runSketch(['hoge'], sketch)


# import pycessing
# class Hoge(pycessing.SketchBase):
#     pass
# pycessing.start(Hoge())
