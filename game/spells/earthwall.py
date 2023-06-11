from game.spell import Spell
from game.stats import Stats

class EarthWall(Spell):
    def __init__(self, x, y, z, uuid):
        super().__init__(x, y, z, "spells/wall", "n", uuid, Stats(), 2)

    def tick(self, dt, isometricRenderer):
        if self.time_elapsed > 30:
            self.done = True

    def on_contact(self, entity):
        pass