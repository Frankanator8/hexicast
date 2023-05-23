from game.spell import Spell
from game.stats import Stats


# TODO: should the server handle logic or should the players?
class Fireball(Spell):
    def __init__(self, x, y, z, sender, direction):
        super().__init__(x, y, z, "spells/fireball", "n", sender, Stats(atk=20, speed=10, range=2, knockback=1), 3)
        self.trueDir = direction