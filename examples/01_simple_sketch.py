import pycessing


# An example of the basic sketch structure
class Sketch(pycessing.SketchBase):
    LINE_RADIUS = 8
    LINE_SPEED = 3

    def setup(self):
        self.size(480, 240)
        self.background(96)
        self.noStroke()

        self.px = self.py = self.LINE_RADIUS
        self.vx = self.vy = self.LINE_SPEED

    def draw(self):
        self.fill(96, 8)
        self.rect(0, 0, self.width, self.height)

        self.px += self.vx
        self.py += self.vy

        if self.px <= self.LINE_RADIUS or self.px >= self.width - self.LINE_RADIUS:
            self.vx *= -1

        if self.py <= self.LINE_RADIUS or self.py >= self.height - self.LINE_RADIUS:
            self.vy *= -1

        self.fill(255, 204, 0)
        self.ellipse(self.px, self.py, self.LINE_RADIUS * 2, self.LINE_RADIUS * 2)


pycessing.start_sketch(Sketch())
