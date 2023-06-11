import math
import time

from game.player import Player
from game.spell import Spell
from game.stats import Stats


class DragonBreath(Spell):
    def __init__(self, x, y, z, player):
        super().__init__(x, y, z, "spells/firewall", "n", player.uuid, Stats(atk=12, speed=10.5), 4)
        self.player = player
        if player.direction == "n":
            self.trueDir = math.radians(270)

        if player.direction == "e":
            self.trueDir = math.radians(0)

        if player.direction == "w":
            self.trueDir = math.radians(180)

        if player.direction == "s":
            self.trueDir = math.radians(90)

        self.hit = []

    def tick(self, dt, isometricRenderer):
        self.x += math.cos(self.trueDir) * self.stats.speed * dt
        self.y += math.sin(self.trueDir) * self.stats.speed * dt

        for player in self.hit:
            player.health -= dt * self.stats.atk/5

        if self.time_elapsed > 10:
            self.done = True


    def on_ground(self):
        self.done = True

    def on_contact(self, entity):
        if len(self.hit) == 0:
            if isinstance(entity, Player):
                if entity.uuid != self.sender:
                    entity.health -= self.stats.atk - entity.stats.defense
                    self.hit.append(entity)
                    self.timeCreated = time.time()

        super().on_contact(entity)

