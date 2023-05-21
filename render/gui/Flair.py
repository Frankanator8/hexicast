import pygame

import loader
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable


class Flair(GuiElement):
    def __init__(self, x, y):
        super().__init__(x, y, [Renderable(loader.load_image("star", size=(0, 0)), (x, y))])
        self.done = False
        self.progress = 0
        self.original = loader.load_image("star")

    def rot_center(self, image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect.topleft

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        self.progress += 180 * dt
        if self.progress >= 360:
            self.done = True
            return


        sized = pygame.transform.scale(self.original, (50*(180-abs(self.progress-180))/180, 50*(180-abs(self.progress-180))/180))
        newSurface, newPos = self.rot_center(sized, self.progress, self.x, self.y)
        newSurface.set_alpha(100)
        self.renderables[0].disp = newSurface
        self.renderables[0].x, self.renderables[0].y = newPos
