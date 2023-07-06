import copy

import pygame

import loader
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable
import random


class UpVisualEffect(GuiElement):
    PARTICLE = 0
    ARROW = 1
    def __init__(self, x, y, type):
        super().__init__(x, y, [])
        self.type = type
        self.done = False
        if self.type == self.PARTICLE:
            size = random.randint(10, 25)
            self.renderables.append(Renderable(pygame.Rect(x, y, size, size), (134, 248, 255), 2))

        else:
            self.opacity = 255
            self.renderables.append(Renderable(loader.load_image("upVFX").copy(), (x, y)))

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        if self.type == self.PARTICLE:
            self.renderables[0].moveTo(self.renderables[0].x, self.renderables[0].y-50*dt)
            self.renderables[0].rect.w -= dt*3
            self.renderables[0].rect.h -= dt*3
            if self.renderables[0].rect.w <= 0:
                self.done = True

        else:
            self.renderables[0].moveTo(self.renderables[0].x, self.renderables[0].y-15*dt)
            self.opacity -=64*dt
            self.renderables[0].disp.set_alpha(self.opacity)
            if self.opacity <= 0:
                self.done = True