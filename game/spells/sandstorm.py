import math

from game.spell import Spell
from game.stats import Stats


class Sandstorm(Spell):
    def __init__(self, x, y, player):
        super().__init__(x, y, math.ceil(player.z)+1, f"spells/sandstorm", "n", player.uuid, Stats(), 4)

    def tick(self, dt, isometricRenderer):
        if self.time_elapsed > 10:
            self.done = True

    def render(self, size):
        surf = super().render(size)
        surf.set_alpha(100)
        return surf