from game.player import Player
from game.spell import Spell
from game.stats import Stats


class PhoenixFlames(Spell):
    def __init__(self, x, y, z, sender):
        super().__init__(x, y, z, "spells/phoenix", "n", sender, Stats(atk=8, healing=5), 3)
        self.players = []

    def tick(self, dt, isometricRenderer):
        for player in self.players:
            if player.uuid == self.sender:
                player.health += self.stats.healing * dt

            else:
                player.health -= (self.stats.atk - player.stats.defense)*dt

        if self.time_elapsed > 8:
            self.done = True

        self.players = []
    def on_contact(self, entity):
        if isinstance(entity, Player):
            self.players.append(entity)
