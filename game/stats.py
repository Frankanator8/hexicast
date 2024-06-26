class Stats:
    def __init__(self, hp=0, maxHP = 0, atk=0, defense=0, speed=0, healing=0, range=1, knockback=0):
        self.hp = hp
        self.maxHP = maxHP
        self.atk = atk
        self.defense = defense
        self.speed = speed
        self.healing = healing
        self.range = range
        self.knockback = knockback

    def getStringRepr(self):
        return f"{self.hp}\n{self.maxHP}\n{self.atk}\n{self.defense}\n{self.speed}\n{self.healing}\n{self.range}\n{self.knockback}"

    def setStringRepr(self, s):
        self.hp, self.maxHP, self.atk, self.defense, self.speed, self.healing, self.range, self.knockback = tuple(s.split())