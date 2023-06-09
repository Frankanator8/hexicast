import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats

class ExplosionFire(Spell):
    def __init__(self, x, y, z, sender):
        super().__init__(x, y, z, "spells/firewall", "n", sender, Stats(atk=20), 3)
        self.players = []

    def on_contact(self, entity):
        if isinstance(entity, Player):
            self.players.append(entity)

    def tick(self, dt, isometricRenderer):
        for player in self.players:
            player.health -= dt * (self.stats.atk-player.stats.defense)

        self.players = []

        if self.time_elapsed > 10:
            self.done = True
class Explosion(Spell):
    def __init__(self, player, spellCreator):
        super().__init__(math.floor(player.x), math.floor(player.y), math.floor(player.z)-1, "spells/explosion", "n", player.uuid,
                         Stats(atk=40), 3)
        self.spellCreator = spellCreator

    def on_contact(self, entity):
        if not isinstance(entity, Explosion):
            if self.time_elapsed > 1.5:
                if isinstance(entity, Player):
                    entity.health -= self.stats.atk - entity.stats.defense

                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i != 0 or j != 0:
                            self.spellCreator.spellManager.addToQueue(ExplosionFire(self.x + i, self.y + j, self.z, self.sender))

                self.done = True
        super().on_contact(entity)
