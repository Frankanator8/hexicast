from game.player import Player
from game.spell import Spell
from game.stats import Stats

class Beam(Spell):
    def __init__(self, x, y, z, dir, sender):
        super().__init__(x, y, z, "spells/beam", dir, sender, Stats(atk=12, range=2, speed=12), 4)

    def tick(self, dt, isometricRenderer):
        if self.direction == "n":
            self.y -= self.stats.speed * dt

        elif self.direction == "s":
            self.y += self.stats.speed * dt

        elif self.direction == "e":
            self.x += self.stats.speed * dt

        else:
            self.x -= self.stats.speed * dt

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                entity.health -= self.stats.atk - entity.stats.defense
                self.done = True
        
        super().on_contact(entity)

    def on_ground(self):
        self.done = True

class SwordOfDestruction(Spell):
    def __init__(self, player, spellCreator):
        super().__init__(player.x, player.y, player.z, "spells/sword", "n", player.uuid,
                         Stats(), 4)
        self.player = player
        self.timeSinceShot = 0
        self.spellCreator = spellCreator

    def tick(self, dt, isometricRenderer):
        self.x = self.player.x
        self.y = self.player.y
        self.z = self.player.z + 1
        if self.time_elapsed > 7:
            self.done = True

        self.timeSinceShot += dt
        if self.timeSinceShot >= 0.8:
            self.timeSinceShot = 0
            dirs = ["n", "s", "e", "w"]
            for dir in dirs:
                for i in range(3):
                    i+=2
                    if dir == "n":
                        self.spellCreator.spellManager.addToQueue(Beam(self.x, self.y-i, self.z, dir, self.sender))

                    elif dir == "s":
                        self.spellCreator.spellManager.addToQueue(Beam(self.x, self.y+i, self.z, dir, self.sender))

                    elif dir == "e":
                        self.spellCreator.spellManager.addToQueue(Beam(self.x+i, self.y, self.z, dir, self.sender))

                    else:
                        self.spellCreator.spellManager.addToQueue(Beam(self.x-i, self.y, self.z, dir, self.sender))

    def on_contact(self, entity):
        pass
