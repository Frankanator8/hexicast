from game.entity import Entity


class Spell(Entity):
    def __init__(self, x, y, z, image, direction, sender, stats, tier):
        super().__init__(x, y, z, image, direction)
        self.sender = sender
        self.done = False
        self.tier = tier
        self.stats = stats

    def on_contact(self, entity):
        pass

    def tick(self, isometricRenderer):
        pass