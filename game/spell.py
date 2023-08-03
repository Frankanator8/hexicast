import time
from game.entity import Entity


class Spell(Entity):
    soundMaster = None
    def __init__(self, x, y, z, image, direction, sender, stats, tier, animation=None):
        super().__init__(x, y, z, image, direction, animation=animation)
        self.sender = sender
        self.done = False
        self.tier = tier
        self.stats = stats
        self.timeCreated = time.time()

    @property
    def time_elapsed(self):
        return time.time() - self.timeCreated

    def on_contact(self, entity):
        if isinstance(entity, Spell):
            if type(self).__name__ != type(entity).__name__:
                if entity != self:
                    if entity.tier >= self.tier:
                        self.done = True

    def on_ground(self):
        pass

    def tick(self, dt, isometricRenderer):
        pass

    def getDictObject(self):
        return {"x":self.x, "y":self.y, "z":self.z, "direction":self.direction, "image":self.image, "sender":self.sender, "tier":self.tier,
                "type":self.__class__.__name__, "stats":self.stats.getStringRepr()}

    def updateFromDictObject(self, obj):
        self.x = obj["x"]
        self.y = obj["y"]
        self.z = obj["z"]
        self.direction = obj["direction"]
        self.image = obj["image"]
        self.sender = obj["sender"]
        self.tier = obj["tier"]
        self.stats.setStringRepr(obj["stats"])