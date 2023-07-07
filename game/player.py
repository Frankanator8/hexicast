from game.entity import Entity
import pygame
import math

from game.stats import Stats
from render.fonts import Fonts
from render.gui.base.text import Text


class Player(Entity):
    def __init__(self, x, y, z, type):
        super().__init__(x, y, z, "p1", "n")
        self.hasPriorityRender = True
        self.type = type
        self.zVel = 0
        self.timeSinceJump = 0
        self.falling = False
        self.uuid = None
        self.name = None
        self.stats = Stats(hp=100, maxHP=100, atk=0, defense=5, speed=8)
        self.hpChange = 0
        self.trueHP = self.stats.hp
        self.me = False
        self.pRender = {"n":{}, "w":{}, "s":{},"e":{},
                        "ni":{}, "wi":{}, "si":{}, "ei":{}}

        self.glowTick = 0
        self.alive = True
        self.show = True

        self.lastPos = (x, y, z)

    def tickKeys(self, keys, prevKeys, dt, map):
        if not self.alive:
            return

        try:
            inWater = map.data[math.floor(self.y)][math.floor(self.x)][math.floor(self.z)-1] == 0

        except IndexError:
            inWater = False

        futPosition = [self.x, self.y]
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            futPosition[1] -= self.stats.speed * dt * (0.5 if inWater else 1)
            self.direction = "n"

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            futPosition[1] += self.stats.speed * dt * (0.5 if inWater else 1)
            self.direction = "s"

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            futPosition[0] -= self.stats.speed * dt * (0.5 if inWater else 1)
            self.direction = "w"

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            futPosition[0] += self.stats.speed * dt * (0.5 if inWater else 1)
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
            if not inWater:
                self.zVel = 5
                self.timeSinceJump = 0

            else:
                surroundingLand = False
                for oY in range(-1, 2):
                    for oX in range(-1, 2):
                        try:
                            if map.data[math.floor(self.y)+oY][math.floor(self.x)+oX][-1] != 0:
                                surroundingLand = True

                        except IndexError:
                            pass

                if surroundingLand:
                    self.zVel = 5
                    self.timeSinceJump = 0

    def renderOffset(self):
        return 0, -40

    def hash(self):
        return f"{self.image}/{self.animation.direction}/{self.animation.animationFrame}" \
               f"{round(self.stats.hp)}-{self.name}-{self.show}-{self.alive}" \
               f"{self.glowTick%6}"

    def render(self, size):
        ret = pygame.Surface((size[0], size[1]+40), pygame.SRCALPHA)
        if self.show:
            ret.blit(super().render(size), (0, 40))
        return ret

    def mixColor(self, color1, color2, proportion):
        return (color1[0] * proportion + color2[0] * (1-proportion),
                color1[1] * proportion + color2[1] * (1-proportion),
                color1[2] * proportion + color2[2] * (1-proportion))

    def prioritizedRender(self, size):
        ret = pygame.Surface((size[0], size[1]+40), pygame.SRCALPHA)
        if self.show:
            t = Text(self.name, Fonts.font18, (50+50*math.sin(self.glowTick), 50+50*math.sin(self.glowTick), 50+50*math.sin(self.glowTick)), (0, 0))
            pygame.draw.rect(ret, (255, 255, 255), pygame.Rect(0, 0, t.w, t.h))
            t.render(ret)
            if self.alive:
                pygame.draw.rect(ret, (116, 116, 116), pygame.Rect(0, 20, size[0], 18), border_radius=5)
                colorMix = self.mixColor((72, 255, 57), (255, 87, 87), self.stats.hp/self.stats.maxHP)
                pygame.draw.rect(ret, colorMix, pygame.Rect(0, 20, size[0] * self.stats.hp/self.stats.maxHP, 18), border_radius=5)
                greenFlashProgress = (self.glowTick%6)/6
                pygame.draw.rect(ret, (min(colorMix[0]+100, 255), min(colorMix[1]+100, 255), min(colorMix[2]+100, 255)), pygame.Rect(0, 25, min(greenFlashProgress*size[0], size[0] * self.stats.hp/self.stats.maxHP), 8), border_radius=0)
                if self.animation.animationFrame not in self.pRender[self.animation.direction].keys():
                    self.pRender[self.animation.direction][self.animation.animationFrame] = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
                    mask = pygame.mask.from_surface(super().render(size))
                    for x, y in mask.outline(every=4):
                        for xO in range(-1, 2):
                            for yO in range(-1, 2):
                                self.pRender[self.animation.direction][self.animation.animationFrame].set_at((x+xO, y+yO), (255, 255, 255))

                ret.blit(self.pRender[self.animation.direction][self.animation.animationFrame], (0, 40))

        return ret

    @property
    def health(self):
        return self.trueHP

    @health.setter
    def health(self, value):
        if value > self.stats.maxHP:
            value = self.stats.maxHP

        self.hpChange += value - self.trueHP
        self.trueHP = value

    def animationTick(self, dt):
        self.glowTick += dt * 2
        if self.falling:
            self.animation.delay = 0.33
            self.animation.tick(dt, self.direction)

        else:
            self.animation.delay = 0.1
            if self.lastPos != (self.x, self.y, self.z):
                self.animation.tick(dt, self.direction)

            else:
                self.animation.tick(dt, f"{self.direction}i")

        self.lastPos = (self.x, self.y, self.z)