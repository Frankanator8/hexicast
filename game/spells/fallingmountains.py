from game.player import Player
from game.spell import Spell
from game.stats import Stats

class FallingMountains(Spell):
    def __init__(self, x, y, z, player):
        super().__init__(x ,y, z, "spells/fallingmountains", "n", player.uuid, Stats(atk=25), 4)
        self.zVel = 0

    def tick(self, dt, isometricRenderer):
        if self.time_elapsed > 0.5:
            self.zVel -= dt * 10

        self.z += self.zVel * dt

    def on_ground(self):
        self.done = True

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                entity.health -= self.stats.atk - entity.stats.defense
                self.done = True