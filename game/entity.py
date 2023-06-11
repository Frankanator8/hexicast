import pygame

import loader


class Entity:
    def __init__(self, x, y, z, image, direction):
        self.x = x
        self.y = y
        self.z = z
        self.image = image
        self.direction = direction

    def render(self, size):
        return loader.load_image(f"{self.image}/{self.direction}", size=size)

    def hash(self):
        return f"{self.image}/{self.direction}"

    def renderOffset(self):
        return 0, 0

    def prioritizedRender(self, size):
        return pygame.Surface((1, 1))