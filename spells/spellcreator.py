import math

from game.spells.fireball import Fireball
from game.spells.firebody import FireBody
from game.spells.phoenixflames import PhoenixFlames


class SpellCreator:
    def __init__(self, spellManager):
        self.element = None
        self.selected = 0
        self.spellManager = spellManager

    def updateElementAndSelected(self, element, selected):
        self.element = element
        self.selected = selected

    def tick(self, player, spellRegister):
        if self.element != None:
            if self.element == "fire":
                if self.selected == 0:
                    self.spellManager.addSpell(FireBody(player))
                    self.element = None

                if self.selected == 3:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                        self.spellManager.isometricRenderer,
                                                        self.spellManager.isometricRenderer.screen)
                        dY = targetY - player.y
                        dX = targetX - player.x
                        dir = math.atan2(dY, dX)
                        self.spellManager.addSpell(Fireball(player.x, player.y, player.z, player.uuid,
                                                            dir))
                        self.element = None

                if self.selected == 4:
                    self.spellManager.addSpell(PhoenixFlames(math.floor(player.x), math.floor(player.y),
                                                             math.floor(player.z)-1, player.uuid))
                    self.element = None
