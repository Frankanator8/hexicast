from game.spell import Spell
from game.stats import Stats

class Rocket(Spell):
    def __init__(self, player):
        super().__init__(player.x, player.y, player.z, "spells/rocket", "n", player.uuid, Stats(), 3)
        self.player = player
        print("i" + str(player.z))
        self.targetZ = player.z + 3

    def tick(self, dt, isometricRenderer):
        player = self.player
        self.x, self.y, self.z = player.x, player.y, player.z
        if player.z < self.targetZ:
            player.zVel = 10

        else:
            player.zVel = 10 * dt

        print(player.z)

        if self.time_elapsed > 6:
            self.done = True

    def on_ground(self):
        self.done = True

