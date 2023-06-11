import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats

class Boulder(Spell):
    def __init__(self, player, dir):
        super().__init__(player.x, player.y, math.floor(player.z), "spells/boulder", "n", player.uuid, Stats(atk=30, speed=6), 3)
        self.trueDir = dir

    def tick(self, dt, isometricRenderer):
        self.x += math.cos(self.trueDir) * self.stats.speed * dt
        self.y += math.sin(self.trueDir) * self.stats.speed * dt

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                degree = (2.5-self.time_elapsed)/2.5
                if degree < 0:
                    degree = 0
                entity.health -= (self.stats.atk - entity.stats.defense) * degree
                self.done = True

        super().on_contact(entity)

    def on_ground(self):
        self.done = True