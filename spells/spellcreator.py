import math

import tools
from game.spells.explosion import Explosion
from game.spells.fireball import Fireball
from game.spells.firebody import FireBody
from game.spells.firewall import Firewall
from game.spells.heatpuff import HeatPuff
from game.spells.phoenixflames import PhoenixFlames


class SpellCreator:
    def __init__(self, spellManager):
        self.element = None
        self.selected = 0
        self.spellManager = spellManager

    def updateElementAndSelected(self, element, selected):
        self.element = element
        self.selected = selected

    def tick(self, player, spellRegister, isometricRenderer):
        if self.element != None:
            if self.element == "fire":
                if self.selected == 0:
                    self.spellManager.addSpell(FireBody(player))
                    self.element = None

                if self.selected == 1:
                    self.spellManager.addSpell(HeatPuff(player))
                    self.element = None

                if self.selected == 2:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, Firewall):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 2:
                                add = False
                    if add:
                        for y in range(-1, 2):
                            for x in range(-1, 2):
                                if x != 0 or y != 0:
                                    self.spellManager.addSpell(Firewall(player.x, player.y, player.z, player, [x, y]))
                    self.element = None

                if self.selected == 3:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                        self.spellManager.isometricRenderer)
                        dY = targetY - player.y
                        dX = targetX - player.x
                        dir = math.atan2(dY, dX)
                        self.spellManager.addSpell(Fireball(player.x, player.y, player.z, player.uuid,
                                                            dir))
                        self.element = None

                if self.selected == 4:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, PhoenixFlames):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 5:
                                add = False
                    if add:
                        self.spellManager.addSpell(PhoenixFlames(math.floor(player.x), math.floor(player.y),
                                                             math.floor(player.z)-1, player.uuid))
                    self.element = None

                if self.selected == 5:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, Explosion):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 3:
                                add = False

                    if add:
                        self.spellManager.addSpell(Explosion(player, self))

                    self.element = None
