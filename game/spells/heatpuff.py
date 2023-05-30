import math

from game.map import Map
from game.spell import Spell
from game.stats import Stats


class HeatPuff(Spell):
    def __init__(self, player):
        super().__init__(math.floor(player.x), math.floor(player.y), math.floor(player.z), "spells/heatpuff", player.direction, player.uuid, Stats(speed=15), 1)
        self.player = player

    def tick(self, dt, isometricRenderer):
        if self.time_elapsed > 1:
            self.done = True

        else:
            futPosition = [self.player.x, self.player.y]
            if self.direction == "n":
                futPosition[1] += self.stats.speed * dt

            elif self.direction == "s":
                futPosition[1] -= self.stats.speed * dt

            elif self.direction == "e":
                futPosition[0] -= self.stats.speed * dt

            elif self.direction == "w":
                futPosition[0] += self.stats.speed * dt

            self.player.x, self.player.y = Map(isometricRenderer.map).findCollisionPoint(*futPosition, self.player)
