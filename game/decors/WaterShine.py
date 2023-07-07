import random

import tools
from game.decor import Decor


class WaterShine(Decor):
    def __init__(self, x, y, z, waters, map):
        super().__init__(x, y, z, "map/waterEntity", "n")
        self.opacity = 0
        self.waitTime = 0
        self.opacityStatus = 0
        self.waters = waters
        self.map = map

    def hash(self):
        return f"{super().hash()}/{self.opacity}"

    def tick(self, player, dt):
        if self.waitTime > 0:
            self.waitTime -= dt

        else:
            if self.opacityStatus == 0:
                possible = []
                for water in self.waters:
                    if tools.dist(player.x, player.y, water[0], water[1]) < 10:
                        possible.append(water)
                if len(possible) > 0:
                    x, y = random.choice(possible)
                    self.x = x
                    self.y = y
                    self.z = len(self.map.data[y][x])-2
                self.opacityStatus = 1
                self.animation.animationFrame = random.randint(0, 9)

            elif self.opacityStatus == 1:
                self.opacity += 255 * dt
                if self.opacity > 255:
                    self.opacity = 255
                    self.opacityStatus = 2

                if tools.dist(player.x, player.y, self.x, self.y) > 10:
                    self.opacity =  random.randint(64, 128)
                    self.opacityStatus = 0
                    self.waitTime = 0

            elif self.opacityStatus == 2:
                self.opacity -= 255 * dt
                if self.opacity < 0:
                    self.opacity = 0
                    self.opacityStatus = 0
                    self.waitTime = random.uniform(0, 0.5)

                if tools.dist(player.x, player.y, self.x, self.y) > 10:
                    self.opacity = random.randint(64, 128)
                    self.opacityStatus = 0
                    self.waitTime = 0

    def render(self, size):
        surf = super().render(size).copy()
        surf.set_alpha(self.opacity)
        return surf

    def animationTick(self, dt):
        pass

