import pygame

from render.fonts import Fonts
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button

class ExitButton(Button):
    def __init__(self, x, y, gameManager, screenMaster):
        super().__init__(x, y, [Renderable(pygame.Rect(x, y, 100, 50), (255, 85, 85), 5),
                                Renderable(Text("Exit", Fonts.font24, (255, 255, 255), (0, 0)))],
                         self.on_hover, self.on_unhover, self.on_click, self.on_release)
        self.renderables[1].text.centerAt(x+50, y+25)
        self.gameManager = gameManager
        self.screenMaster = screenMaster

    def on_hover(self):
        self.renderables[0].color = (255, 161, 161)

    def on_unhover(self):
        self.renderables[0].color = (255, 85, 85)

    def on_click(self):
        self.renderables[0].rect.x += 8
        self.renderables[0].rect.y += 8
        self.renderables[0].rect.w -= 16
        self.renderables[0].rect.h -= 16
        self.recalculateWH()

    def on_release(self):
        self.renderables[0].rect.x -= 8
        self.renderables[0].rect.y -= 8
        self.renderables[0].rect.w += 16
        self.renderables[0].rect.h += 16
        self.recalculateWH()
        self.gameManager.reset()
        self.screenMaster.screenID = 1