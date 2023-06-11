from game.spell import Spell
from game.stats import Stats


class FireBody(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, player.z, "spells/firebody", "n", player.uuid, Stats(speed=10.5), 1)
        self.player = player

    def tick(self, dt, isometricRenderer):
        self.direction = self.player.direction
        if self.direction == "n":
            self.x = self.player.x
            self.y = self.player.y-1

        elif self.direction == "s":
            self.x = self.player.x
            self.y = self.player.y+1

        elif self.direction == "w":
            self.x = self.player.x-1
            self.y = self.player.y

        else:
            self.x = self.player.x+1
            self.y = self.player.y
        self.z = self.player.z
        self.player.stats.speed = self.stats.speed
        if self.time_elapsed > 3:
            self.done = True
            self.player.stats.speed = 8
    def on_contact(self, entity):
        pass

