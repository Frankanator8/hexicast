import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats

class WaterBlast(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, math.floor(player.z), "spells/waterblast", player.direction, player.uuid, Stats(atk=20, speed=10), 3)
        if player.direction == "n":
            self.trueDir = math.radians(270)

        if player.direction == "e":
            self.trueDir = math.radians(0)

        if player.direction == "w":
            self.trueDir = math.radians(180)

        if player.direction == "s":
            self.trueDir = math.radians(90)

    def tick(self, dt, isometricRenderer):
        self.x += math.cos(self.trueDir) * self.stats.speed * dt
        self.y += math.sin(self.trueDir) * self.stats.speed * dt

    def on_ground(self):
        self.done = True

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                entity.health -= self.stats.atk - entity.stats.defense
                self.done = True

        super().on_contact(entity)