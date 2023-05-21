import pygame

from render.gui.base.text import Text


class Renderable:
    def __init__(self, *args):
        self.w = 0
        self.h = 0
        self.x = 0
        self.y = 0
        if isinstance(args[0], pygame.Surface):
            self.type = 0
            self.disp = args[0]
            self.x, self.y = args[1]
            self.w = args[0].get_width()
            self.h = args[0].get_height()

        elif isinstance(args[0], pygame.Rect):
            self.type = 1
            self.rect = args[0]
            self.color = args[1]
            self.radius = args[2]
            self.w = args[0].w
            self.h = args[0].h
            self.x = args[0].x
            self.y = args[0].y

        elif isinstance(args[0], Text):
            self.type = 2
            self.text = args[0]
            self.x = args[0].pos[0]
            self.y = args[0].pos[1]
            self.w, self.h = (args[0].w, args[0].h)

    def render(self, screen):
        if self.type == 0:
            screen.blit(self.disp, (self.x, self.y))

        elif self.type == 1:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=self.radius)

        else:
            self.text.render(screen)

    def moveTo(self, x, y):
        if self.type == 0:
            self.x = x
            self.y = y

        elif self.type == 1:
            self.rect.x = x
            self.rect.y = y

        else:
            self.text.pos = (x, y)

        self.x = x
        self.y = y
