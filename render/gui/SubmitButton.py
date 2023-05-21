import pygame

from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button


class SubmitButton(Button):
    def __init__(self, x, y, w, h, font, on_release, text="Submit"):
        textDummy = Text(text, font, (0, 0, 0), (x, y))
        self.releaseFunc = on_release
        self.origW = w
        self.origH = h
        super().__init__(x, y, [Renderable(pygame.Rect(x, y, w, h), (255, 183, 58), (w+h)//2),
                                Renderable(Text(text, font, (0, 0, 0), (x+(w-textDummy.w)/2, y+(h-textDummy.h)/2)))], self.hover, self.unhover, self.click, self.release)

    def hover(self):
        self.renderables[0].color = (255, 200, 103)

    def unhover(self):
        self.renderables[0].color = (255, 183, 58)

    def click(self):
        renderObjs = []
        renderObjs.append(Renderable(pygame.Rect(self.x+2, self.y+2, self.origW-4, self.origH-4), (255, 183, 58), round((self.w+self.h)//2)))
        renderObjs.append(self.renderables[1])
        self.renderables = renderObjs
        self.recalculateWH()

    def release(self):
        renderObjs = []
        renderObjs.append(Renderable(pygame.Rect(self.x, self.y, self.origW, self.origH), (255, 183, 58), round((self.origW+self.origH)//2)))
        renderObjs.append(self.renderables[1])
        self.renderables = renderObjs
        self.recalculateWH()
        self.releaseFunc()
