import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats


class Firewall(Spell):
    def __init__(self, x, y, z, player, offsets):
        super().__init__(x, y, z, "spells/firewall", "n", player.uuid, Stats(atk=12), 2)
        self.players = []
        self.player = player
        self.offsets = offsets

    def tick(self, dt, isometricRenderer):
        for player in self.players:
            player.health -= dt * self.stats.atk

        if self.time_elapsed > 5:
            self.done = True

        self.x = math.floor(self.player.x) + self.offsets[0]
        self.y = math.floor(self.player.y) + self.offsets[1]
        self.z = self.player.z-1
        self.players = []

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                self.players.append(entity)
        super().on_contact(entity)