import pygame

from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button


class GameButton(Button):
    def __init__(self, x, y, game, color, font, screen_width):
        super().__init__(x, y, [Renderable(pygame.Rect(x, y, screen_width-x-10, font[1]*2+2), color, 3),
                                Renderable(Text(f"{game['name']} - {len(game['players'])}/{game['settings']['maxPlayers']}\nHost:{game['host']}", font, (0, 0, 0), (x+1, y+1)))],
                         lambda:None,lambda:None,lambda:None,lambda:None)


