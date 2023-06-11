import math

from game.spell import Spell
from game.stats import Stats


class Footsteps(Spell):
    def __init__(self, x, y, z, dir, uuid):
        super().__init__(x, y, z, "spells/footsteps", self.getDisplayDirection(dir), uuid, Stats(), 2)

    @staticmethod
    def getDisplayDirection(direction):
        pi = math.pi
        if direction < 0:
            direction += math.pi * 2
        if pi/4 < direction <= 3*pi/4:
            return "n"

        elif 3*pi/4<direction<=5*pi/4:
            return "w"

        elif 5*pi/4<direction<=7*pi/4:
            return "s"

        else:
            return "e"

    def tick(self, dt, isometricRenderer):
        if self.time_elapsed > 3:
            self.done = True