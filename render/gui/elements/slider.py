import pygame

from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable


class Slider(GuiElement):
    def __init__(self, x, y, w, h, initialValue, valueFunction):
        self.value = initialValue
        self.width = w
        self.height = h
        self.prevMouseX = -1
        self.valueFunction = valueFunction
        super().__init__(x, y, [Renderable(pygame.Rect(x, y+h/4, w, h/2), (0, 0, 0), 5),
                                Renderable(pygame.Rect(self.value/100*9/10*self.width+x, y, w/10, h), (34, 163, 227), 8)])

    def calcX(self):
        return self.value/100*9/10*self.width+self.x

    def calcValue(self, x):
        x -= self.x
        value = (x / (9/10*self.width)) * 100
        if value > 100:
            value = 100

        if value < 0:
             value = 0

        return value

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        if mouseClicked[0]:
            if self.prevMouseX != -1:
                self.value = self.calcValue(self.calcX()+(mousePos[0]-self.prevMouseX))
                self.prevMouseX = mousePos[0]

            else:
                if self.calcX() <= mousePos[0] <= self.calcX() + self.width/10 and self.y <= mousePos[1] <= self.y + self.height:
                    if not prevClicked[0]:
                        self.prevMouseX = mousePos[0]

                    else:
                        self.prevMouseX = -1

                else:
                    self.prevMouseX = -1

        else:
            self.prevMouseX = -1

        self.renderables[1].rect.x = self.calcX()
        self.renderables[1].x = self.calcX()
        self.valueFunction(self.value)