import pygame

import loader
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable


class ScrollingBackground(GuiElement):
    def __init__(self, image, x, y, speed=1):
        self.img = loader.load_image(image)
        self.renderImg = pygame.Surface(self.img.get_size(), pygame.SRCALPHA)
        super().__init__(x, y, [Renderable(self.renderImg, (x, y))])
        self.image = image
        self.prog = 0
        self.speed = speed

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        self.prog += dt * self.speed
        self.prog %= 1
        xO = self.prog * self.renderImg.get_width()
        yO = self.prog * self.renderImg.get_height()
        self.renderImg.fill((0, 0, 0))
        self.renderImg.blit(self.img, (xO, yO))
        self.renderImg.blit(self.img, (xO-self.img.get_width(), yO))
        self.renderImg.blit(self.img, (xO-self.img.get_width(), yO-self.img.get_height()))
        self.renderImg.blit(self.img, (xO, yO-self.img.get_height()))
