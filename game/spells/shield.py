import math

from game.spell import Spell
from game.stats import Stats

class Shield(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, player.z, "spells/shield", player.direction, player.uuid, Stats(), 1)
        self.player = player
        self.setHealth = player.health

    def tick(self, dt, isometricRenderer):
        self.x = self.player.x
        self.y = self.player.y
        self.z = self.player.z
        self.direction = self.player.direction
        if self.player.health < self.setHealth:
            self.player.health = self.setHealth

        else:
            self.setHealth = self.player.health

        if self.time_elapsed > 7:
            self.done = True

    def on_contact(self, entity):
        pass
