import math

from game.spell import Spell
from game.stats import Stats


class Freeze(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, player.z, "spells/freeze", "n", player.uuid, Stats(defense=12), 1)
        self.player = player

    def tick(self, dt, isometricRenderer):
        self.direction = self.player.direction
        self.x = self.player.x
        self.y = self.player.y
        self.z = math.floor(self.player.z)
        self.player.stats.defense = self.stats.defense
        if self.time_elapsed > 3:
            self.done = True
            self.player.stats.defense = 5
    def on_contact(self, entity):
        pass