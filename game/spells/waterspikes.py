from game.player import Player
from game.spell import Spell
from game.stats import Stats


class WaterSpikes(Spell):
    def __init__(self, x, y, z, sender):
        super().__init__(x, y, z, "spells/waterspikes", "n", sender, Stats(atk=4), 2)
        self.attacking = False

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                if self.attacking:
                    entity.health -= self.stats.atk - entity.stats.defense
                    self.done = True

    def tick(self, dt, isometricRenderer):
        if self.time_elapsed > 1:
            self.attacking = True

        if self.time_elapsed > 2:
            self.done = True
