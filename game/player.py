from game.entity import Entity
import pygame
import math

class Player(Entity):
    def __init__(self, x, y, z, type):
        super().__init__(x, y, z, "p1", "n")
        self.type = type
        self.zVel = 0
        self.timeSinceJump = 0
        self.falling = False

    def tickKeys(self, keys, prevKeys, dt, map):
        futPosition = [self.x, self.y]
        if keys[pygame.K_UP]:
            futPosition[1] -= 8 * dt
            self.direction = "n"

        elif keys[pygame.K_DOWN]:
            futPosition[1] += 8 * dt
            self.direction = "s"

        elif keys[pygame.K_LEFT]:
            futPosition[0] -= 8 * dt
            self.direction = "w"

        elif keys[pygame.K_RIGHT]:
            futPosition[0] += 8 * dt
            self.direction = "e"

        self.x, self.y = map.findCollisionPoint(futPosition[0], futPosition[1], self)
        if self.z > len(map.data[math.floor(self.y)][math.floor(self.x)]):
            self.zVel -= 10 * dt
            self.falling = True

        self.z += self.zVel * dt
        if self.z < len(map.data[math.floor(self.y)][math.floor(self.x)]):
            self.zVel = 0
            self.z = len(map.data[math.floor(self.y)][math.floor(self.x)])
            self.falling = False

        if keys[pygame.K_SPACE] and not prevKeys[pygame.K_SPACE] and not self.falling:
            self.zVel = 5
            self.timeSinceJump = 0


