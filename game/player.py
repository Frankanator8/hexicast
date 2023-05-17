from game.entity import Entity
import pygame

class Player(Entity):
    def __init__(self, x, y, z, type):
        super().__init__(x, y, z, "p1", "n")
        self.type = type

    def tickKeys(self, keys, dt):
        if keys[pygame.K_UP]:
            self.y -= 2 * dt
            self.direction = "n"

        elif keys[pygame.K_DOWN]:
            self.y += 2 * dt
            self.direction = "s"

        elif keys[pygame.K_LEFT]:
            self.x -= 2 * dt
            self.direction = "w"

        elif keys[pygame.K_RIGHT]:
            self.x += 2 * dt
            self.direction = "e"