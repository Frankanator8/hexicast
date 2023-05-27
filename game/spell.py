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

    def tick(self, dt, isometricRenderer):
        pass

    def getDictObject(self):
        return {"x":self.x, "y":self.y, "z":self.z, "direction":self.direction, "image":self.image, "sender":self.sender, "tier":self.tier}