import loader
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable


class Pulse(GuiElement):
    def __init__(self, x, y, image, duration, offset=0):
        super().__init__(x, y, [Renderable(image.copy(), (x, y))])
        self.opacity = 0
        self.duration = duration
        self.time = offset

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        self.time += dt
        if self.time > self.duration:
            self.time = 0
            self.opacity = 255

        self.opacity -= 255 * dt/self.duration
        self.renderables[0].disp.set_alpha(self.opacity)