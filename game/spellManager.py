import copy
import math
import uuid as UUID

from game.spell import Spell
from game.stats import Stats


class SpellManager:
    def __init__(self, isometricRenderer):
        self.spells = {}
        self.isometricRenderer = isometricRenderer
        self.unsentSpells = {}
        self.removeSpells = {}

        self.spellPoses = {}
        self.trueSpellPoses = {}

        self.spellQueue = []

    def reset(self):
        self.spells = {}
        self.unsentSpells = {}
        self.removeSpells = {}
        self.spellQueue = []

    def addToQueue(self, spell):
        self.spellQueue.append(spell)

    def addSpell(self, spell):
        uuid = str(UUID.uuid4())
        self.spells[uuid] = spell
        self.isometricRenderer.addEntity(spell)

    def removeSpell(self, spellUuid):
        self.isometricRenderer.removeEntity(self.spells[spellUuid])
        self.removeSpells[spellUuid] = self.spells[spellUuid]
        del self.spells[spellUuid]

    def tick(self, gameNetworking, dt, ticks):
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

            if value["sender"] != gameNetworking.uuid:
                add = False
                if key not in self.spells.keys() and key not in self.removeSpells.keys():
                    self.isometricRenderer.addEntity(spell)
                    add = True

                if add:
                    self.spells[key] = spell
                    self.spellPoses[key] = []
                    self.trueSpellPoses[key] = (value["x"], value["y"], value["z"])

                else:
                    passObj = copy.deepcopy(value)
                    if (value["x"], value["y"], value["z"]) != self.trueSpellPoses[key]:
                        passObj["x"], passObj["y"], passObj["z"] = self.trueSpellPoses[key]
                        if ticks < 1:
                            ticks = 1

                        self.spellPoses[key] = []
                        for i in range(1, ticks+1):
                            self.spellPoses[key].append((passObj["x"] + i/ticks * (value["x"]-passObj["x"]), passObj["y"] + i/ticks * (value["y"]-passObj["y"]), passObj["z"] + i/ticks * (value["z"]-passObj["z"])))

                        self.trueSpellPoses[key] = (value["x"], value["y"], value["z"])

                    if len(self.spellPoses[key]) > 0:
                        passObj["x"], passObj["y"], passObj["z"] = self.spellPoses[key][0]
                        self.spellPoses[key].pop(0)
                    self.spells[key].updateFromDictObject(passObj)

        removeSpells = []
        for uuid, spell in self.spells.items():
            if spell.sender == gameNetworking.uuid:
                if spell.y < 0 or spell.y >= len(self.isometricRenderer.map.data) or spell.x < 0 or spell.x >= len(
                        self.isometricRenderer.map.data[math.floor(spell.y)]):
                    spell.done = True

                else:
                    isoRenderer = self.isometricRenderer
                    for entity in isoRenderer.entities:
                        if not (entity.x > spell.x + spell.stats.range or entity.x + 1 < spell.x - (
                                spell.stats.range - 1)
                                or entity.y > spell.y + spell.stats.range or entity.y + 1 < spell.y - (
                                        spell.stats.range - 1)
                                or entity.z > spell.z + spell.stats.range or entity.z + 1 < spell.z - (
                                        spell.stats.range - 1)):
                            spell.on_contact(entity)

                    if spell.z+1 < len(isoRenderer.map.data[math.floor(spell.y)][math.floor(spell.x)]):
                        spell.on_ground()

            if spell.done:
                removeSpells.append(uuid)

        for spell in removeSpells:
            self.removeSpell(spell)

        for spell in self.spellQueue:
            self.addSpell(spell)

        self.spellQueue = []
