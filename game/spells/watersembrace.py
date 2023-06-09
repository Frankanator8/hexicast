import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats

class WatersEmbrace(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, math.floor(player.z)-1, "spells/embrace", "n", player.uuid,
                         Stats(healing=8), 3)
        self.player = player

    def tick(self, dt, isometricRenderer):
        self.player.health += self.stats.healing * dt
        self.x = self.player.x
        self.y = self.player.y
        self.z = self.player.z
        if self.time_elapsed > 4:
            self.done = True
