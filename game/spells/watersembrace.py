import math

from game.spell import Spell
from game.stats import Stats
from render.EntityAnimation import EntityAnimation


class WatersEmbrace(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, math.floor(player.z)-1, "spells/embrace", "n", player.uuid,
                         Stats(healing=8), 3, animation=EntityAnimation("spells/embrace", 0.1, EntityAnimation.BOUNCE, "n"))
        self.player = player

    def tick(self, dt, isometricRenderer):
        self.player.health += self.stats.healing * dt
        self.x = self.player.x
        self.y = self.player.y
        self.z = self.player.z
        if self.time_elapsed > 4:
            self.done = True
