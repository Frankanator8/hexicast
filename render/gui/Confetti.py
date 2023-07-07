import math
import random

import pygame

from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable


class Confetti(GuiElement):
    def __init__(self, x, y, color, size):
        self.renderImg = pygame.Surface((size, size), pygame.SRCALPHA)
        super().__init__(x, y, [Renderable(self.renderImg, (x, y))])
        self.rotation = 0
        self.color = color

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        self.rotation += dt * 3.14 * random.uniform(0.5, 2)
        self.renderImg.fill((255, 255, 255, 0))
        pygame.draw.arc(self.renderImg, self.color, pygame.Rect(0, 0, *self.renderImg.get_size()), self.rotation, self.rotation+math.pi/6, width=10)
        self.moveTo(self.x, self.y + dt*200)
