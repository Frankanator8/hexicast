import uuid as UUID

from game.spell import Spell
from game.stats import Stats


class SpellManager:
    def __init__(self, isometricRenderer):
        self.spells = {}
        self.isometricRenderer = isometricRenderer
        self.unsentSpells = {}
        self.removeSpells = {}

    def addSpell(self, spell):
        uuid = str(UUID.uuid4())
        self.spells[uuid] = spell
        self.isometricRenderer.addEntity(spell)

    def removeSpell(self, spellUuid):
        self.removeSpells[spellUuid] = self.spells[spellUuid]
        del self.spells[spellUuid]

    def tick(self, gameNetworking, dt):
        for spell in self.spells.values():
            spell.tick(dt, self.isometricRenderer)

        for uuid, spell in self.spells.items():
            if spell.sender == gameNetworking.uuid:
                self.unsentSpells[uuid] = spell


        keysToDelete = []
        for key in self.spells.keys():
            if key not in gameNetworking.gameData["gameData"]["spells"].keys():
                if key not in self.unsentSpells.keys():
                    self.isometricRenderer.removeEntity(self.spells[key])
                    keysToDelete.append(key)

        for key in keysToDelete:
            del self.spells[key]

        for key, value in gameNetworking.gameData["gameData"]["spells"].items():
            spell = Spell(value["x"], value["y"], value["z"], value["image"], value["direction"], value["sender"],
                          Stats(), value["tier"])
            if key not in self.spells.keys():
                self.isometricRenderer.addEntity(spell)

            if value["sender"] != gameNetworking.uuid:
                self.spells[key] = spell
