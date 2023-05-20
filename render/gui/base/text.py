import pygame

class Text: # allows for renderable text
    def __init__(self, text, font, color, pos):
        self.text = text
        self.font = font
        self.color = color
        self.pos = pos
        self.w = 0
        self.h = 0
        self.make_font()

    def set_text(self, newtext):
        self.text = newtext
        self.make_font()

    def set_color(self, newColor):
        self.color = newColor
        self.make_font()

    def make_font(self):
        font = self.font[0]
        if not isinstance(self.font[0], pygame.font.Font):
            font = pygame.font.SysFont(self.font[0], self.font[1])


        if "\n" in self.text:
            texts = self.text.split("\n")
            self.font_render = []
            maxW = 0
            for text in texts:
                self.font_render.append(font.render(text, True, self.color, None))
                if self.font_render[-1].get_width() > maxW:
                    maxW = self.font_render[-1].get_width()
            self.w = maxW
            self.h = (len(texts)-1) * (self.font[1] + 2) + self.font_render[-1].get_height()

        else:
            self.font_render = font.render(self.text, True, self.color, None)
            self.w = self.font_render.get_width()
            self.h = self.font_render.get_height()

    def render(self, screen):
        if type(self.font_render) != list:
            screen.blit(self.font_render, self.pos)

        else:
            for index, render in enumerate(self.font_render):
                screen.blit(render, (self.pos[0], self.pos[1] + index * (self.font[1] + 2)))

