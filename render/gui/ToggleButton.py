import pygame

from audio.soundlibrary import SoundLibrary
from render.fonts import Fonts
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button


class ToggleButton(Button):
    soundMaster = None
    def __init__(self, x, y, text, default_value=False):
        self.textW = Text(text, Fonts.font18, (0, 0, 0), (x, y)).w
        super().__init__(x, y, [Renderable(Text(text, Fonts.font18, (0, 0, 0), (x, y))),
                                Renderable(pygame.Rect(x+10+self.textW, y, 50, 25), (213, 213, 213), 13),
                                Renderable(pygame.Rect(x+10+self.textW, y, 25, 25), (255, 255, 255), 13)], lambda:None, lambda:None, lambda:None, self.release)
        self.value = default_value

    def release(self):
        self.value = not self.value
        self.soundMaster.playSound(SoundLibrary.CLICK)

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        super().tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        if self.value:
            self.renderables[1].color = (124, 255, 54)
            self.renderables[2].moveTo(self.x+10+self.textW+25, self.y)

        else:
            self.renderables[1].color = (213, 213, 213)
            self.renderables[2].moveTo(self.x+10+self.textW, self.y)
