from game.player import Player
from game.spell import Spell
from game.stats import Stats
import math

# TODO: should the server handle logic or should the players?
class Fireball(Spell):
    def __init__(self, x, y, z, sender, direction):
        super().__init__(x, y, z, "spells/fireball", "n", sender, Stats(atk=20, speed=5, range=2, knockback=1), 3)
        self.trueDir = direction

    def tick(self, dt, isometricRenderer):
        self.x += math.cos(self.trueDir) * self.stats.speed * dt
        self.y += math.sin(self.trueDir) * self.stats.speed * dt

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                entity.stats.hp -= self.stats.atk - entity.stats.defense
                self.done = True
