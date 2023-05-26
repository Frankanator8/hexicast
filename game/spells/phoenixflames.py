from game.spell import Spell
from game.stats import Stats


class PhoenixFlames(Spell):
    def __init__(self, x, y, z, sender):
        super().__init__(x, y, z, "spells/phoenix", "n", sender, Stats(atk=5, healing=5), 3)
