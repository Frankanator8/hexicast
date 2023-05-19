from game.entity import Entity
import pygame
import math

class Player(Entity):
    def __init__(self, x, y, z, type):
        super().__init__(x, y, z, "p1", "n")
        self.type = type
        self.zVel = 0
        self.timeSinceJump = 0
        self.jumping = False

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

        # TODO: Fix Jumping
        if self.z > len(map.data[math.floor(self.y)][math.floor(self.x)]):
            self.zVel -= 16 * dt * dt

        else:
            self.zVel = 0
            self.z = len(map.data[math.floor(self.y)][math.floor(self.x)])

        if keys[pygame.K_SPACE] and not prevKeys[pygame.K_SPACE]:
            self.zVel = 1
            self.timeSinceJump = 0

        self.z += self.zVel



        self.x, self.y = map.findCollisionPoint(futPosition[0], futPosition[1], self)