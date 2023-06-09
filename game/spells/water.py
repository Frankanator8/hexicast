import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats


class Water(Spell):
    def __init__(self, x, y, player, direction, spellCreator, move=True):
        super().__init__(x, y, math.floor(player.z), "spells/water", self.getDisplayDirection(direction), player.uuid,
                         Stats(atk=10, speed=30), 4)
        self.trueDir = direction
        self.player = player
        self.move = move
        self.players = []
        self.spellCreator = spellCreator
        self.added = set()

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                self.players.append(entity)

        super().on_contact(entity)

    def tick(self, dt, isometricRenderer):
        for player in self.players:
            player.health -= (self.stats.atk - player.stats.defense) * dt

        self.players = []
        if self.move:
            self.x += math.cos(self.trueDir) * self.stats.speed * dt
            self.y += math.sin(self.trueDir) * self.stats.speed * dt
            placeX = math.floor(self.x)
            placeY = math.floor(self.y)
            for j in range(-1, 2):
                for i in range(-1, 2):
                    if (placeX+i, placeY+j) not in self.added:
                        self.spellCreator.spellManager.addToQueue(Water(placeX+i, placeY+j, self.player, self.trueDir, self.spellCreator, move=False))
                        self.added.add((placeX+i, placeY+j))

        if self.time_elapsed > 15:
            self.done = True

    def on_ground(self):
        self.done = True


    def getDisplayDirection(self, direction):
        pi = math.pi
        if pi/4 < direction <= 3*pi/4:
            return "n"

        elif 3*pi/4<direction<=5*pi/4:
            return "w"

        elif 5*pi/4<direction<7*pi/4:
            return "s"

        else:
            return "e"
