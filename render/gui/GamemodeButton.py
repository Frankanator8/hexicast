import math

import pygame

import loader
from render.fonts import Fonts
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button

class GamemodeButton(Button):
    CHALLENGE = "challenge"
    LADDER = "ladder"
    PRIVATE = "private"
    DESCS = {
        LADDER: "1v1 rated fun! Automatically queues you into a game",
        CHALLENGE: "Rated or unrated fun, with you choosing the game!",
        PRIVATE: "Unrated fun, create private game lobbies!"
    }
    COLORS = {
        LADDER: (228, 0, 0),
        CHALLENGE: (152, 0, 228),
        PRIVATE: (0, 155, 228)
    }
    SECONDARY = {
        LADDER: (228, 116, 116),
        CHALLENGE: (197, 82, 255),
        PRIVATE: (103, 206, 255)
    }
    def __init__(self, x, y, w, h, challengeType, func):
        super().__init__(x, y, [Renderable(pygame.Rect(x, y, w, h), self.COLORS[challengeType], 5),
                                Renderable(loader.load_image(challengeType, size=(h-10, h-10)), (x+5, y+5)),
                                Renderable(Text(challengeType.capitalize(), Fonts.font48, (0, 0, 0), (x+5+h-10, y+5))),
                                Renderable(Text(self.DESCS[challengeType], Fonts.font18, (0, 0, 0), (x+5+h-10, y+5+Text(challengeType, Fonts.font48, (0, 0, 0), (x+5+h-10, y+5)).h)))],
                         lambda:None, lambda:None, lambda:None, func)
        self.func = func
        self.challengeType = challengeType
        self.colorFluc = 0
        self.trueRect = pygame.Rect(x, y, w, h)

    def mixColor(self, color1, color2, proportion):
        return (color1[0] * proportion + color2[0] * (1-proportion),
                color1[1] * proportion + color2[1] * (1-proportion),
                color1[2] * proportion + color2[2] * (1-proportion))

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        super().tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        if self.hover:
            self.colorFluc += dt*4

        else:
            self.colorFluc = 0

        self.renderables[0].color = self.mixColor(self.COLORS[self.challengeType], self.SECONDARY[self.challengeType],
                                                  (1+math.cos(self.colorFluc))/2)

        if self.click:
            self.renderables[0].rect = pygame.Rect(self.trueRect.x-3, self.trueRect.y-3, self.trueRect.w+6, self.trueRect.h+6)

        else:
            self.renderables[0].rect = self.trueRect

