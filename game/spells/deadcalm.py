import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats

class DeadCalm(Spell):
    def __init__(self, player, x, y):
        super().__init__(x, y, math.floor(player.z)-1, "spells/deadcalm", "n", player.uuid, Stats(atk=10), 4)
        self.players = []
        self.player = player
        self.pos = (player.x, player.y, player.z)

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                self.players.append(entity)

        if isinstance(entity, Spell):
            if entity.sender != self.sender:
                self.done = True

    def tick(self, dt, isometricRenderer):
        for player in self.players:
            player.health -= (self.stats.atk - player.stats.defense) * dt
        self.players = []
        self.player.x, self.player.y, self.player.z = self.pos
        if self.time_elapsed > 6:
            self.done = True