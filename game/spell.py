import time
from game.entity import Entity


class Spell(Entity):
    def __init__(self, x, y, z, image, direction, sender, stats, tier):
        super().__init__(x, y, z, image, direction)
        self.sender = sender
        self.done = False
        self.tier = tier
        self.stats = stats
        self.timeCreated = time.time()

    @property
    def time_elapsed(self):
        return time.time() - self.timeCreated

    def on_contact(self, entity):
        pass

    def tick(self, dt, isometricRenderer):
        pass

    def getDictObject(self):
        return {"x":self.x, "y":self.y, "z":self.z, "direction":self.direction, "image":self.image, "sender":self.sender, "tier":self.tier}

    def updateFromDictObject(self, obj):
        self.x = obj["x"]
        self.y = obj["y"]
        self.z = obj["z"]
        self.direction = obj["direction"]
        self.image = obj["image"]
        self.sender = obj["sender"]
        self.tier = obj["tier"]