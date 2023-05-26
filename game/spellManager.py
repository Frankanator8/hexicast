import uuid as UUID
class SpellManager:
    def __init__(self, isometricRenderer):
        self.spells = {}
        self.isometricRenderer = isometricRenderer
        self.unsentSpells = {}

    def addSpell(self, spell):
        uuid = str(UUID.uuid4())
        self.spells[uuid] = spell
        self.unsentSpells[uuid] = spell
        self.isometricRenderer.addEntity(spell)

    def tick(self, dt):
        for spell in self.spells.values():
            spell.tick(dt, self.isometricRenderer)


