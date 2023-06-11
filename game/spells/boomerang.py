import math

import tools
from game.player import Player
from game.spell import Spell
from game.stats import Stats


class Boomerang(Spell):
    def __init__(self, player, dest):
        super().__init__(player.x, player.y, math.floor(player.z), "spells/boomerang", "n", player.uuid,
                         Stats(atk=20, speed=15),
                         1)
        self.dest = dest
        self.hit = set()
        self.going = True
        self.player = player

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                if entity not in self.hit:
                    entity.health -= self.stats.atk - entity.stats.defense
                    self.hit.add(entity)

        super().on_contact(entity)

    def on_ground(self):
        self.done = True

    def tick(self, dt, isometricRenderer):
        if self.going:
            dest = self.dest

        else:
            dest = (self.player.x, self.player.y)

        if tools.dist(self.x, self.y, *dest) < 1:
            if self.going:
                self.going = False

            else:
                self.done = True

        else:
            dY = dest[1] - self.y
            dX = dest[0] - self.x
            dir = math.atan2(dY, dX)
            self.direction = self.getDisplayDirection(dir)
            self.x += math.cos(dir) * self.stats.speed * dt
            self.y += math.sin(dir) * self.stats.speed * dt

    def getDisplayDirection(self, direction):
        pi = math.pi
        if pi/4 < direction <= 3*pi/4:
            return "n"

        elif 3*pi/4<direction<=5*pi/4:
            return "w"

        elif 5*pi/4<direction<7*pi/4:
            return "s"

        else:
            return "e"