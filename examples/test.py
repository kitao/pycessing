import pycessing


class App(pycessing.App):
  def setup(self):
    self.size(400, 300)

  def draw(self):
    self.background(128, 0, 0)
    self.fill(0, 255, 0)
    self.rect(100, 100, 100, 100)


pycessing.run_app(App(title='hoge', pos=(200, 400), topmost=True))
