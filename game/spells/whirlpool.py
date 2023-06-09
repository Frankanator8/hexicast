import math

from game.player import Player
from game.spell import Spell
from game.stats import Stats

class Whirlpool(Spell):
    def __init__(self, player, radius, degree):
        super().__init__(player.x, player.y, math.floor(player.z), "spells/water", "n", player.uuid, Stats(atk=30, speed=180), 4)
        self.degree = degree
        self.radius = radius
        self.renderRadius = 0
        self.player = player
        self.players = []

    def on_contact(self, entity):
        if isinstance(entity, Player):
            if entity.uuid != self.sender:
                self.players.append(entity)

    def tick(self, dt, isometricRenderer):
        for player in self.players:
            player.health -= (self.stats.atk - player.stats.defense) * dt
        self.players = []

        if self.renderRadius < self.radius:
            self.renderRadius += dt * self.radius

        else:
            self.renderRadius = self.radius

        player = self.player

        self.x = player.x + math.cos(math.radians(self.degree)) * self.renderRadius
        self.y = player.y + math.sin(math.radians(self.degree)) * self.renderRadius
        self.z = math.floor(player.z)
        self.degree += dt * self.stats.speed
        self.direction = self.getDisplayDirection(math.radians(self.degree))
        if self.time_elapsed > 10:
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