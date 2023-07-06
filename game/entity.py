import pygame

import loader
from render.EntityAnimation import EntityAnimation


class Entity:
    def __init__(self, x, y, z, image, direction, animation=None):
        self.x = x
        self.y = y
        self.z = z
        self.image = image
        if animation is None:
            self.animation = EntityAnimation(image, 0.1, EntityAnimation.LOOP, direction)

        else:
            self.animation = animation

        self.direction = direction

    def render(self, size):
        return self.animation.get_image(size=size)

    def hash(self):
        return f"{self.image}/{self.animation.direction}/{self.animation.animationFrame}"

    def renderOffset(self):
        return 0, 0

    def prioritizedRender(self, size):
        return pygame.Surface((1, 1))

    def animationTick(self, dt):
        self.animation.tick(dt, self.direction)