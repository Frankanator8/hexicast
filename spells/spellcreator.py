import math

import tools
from game.spells.boomerang import Boomerang
from game.spells.boulder import Boulder
from game.spells.deadcalm import DeadCalm
from game.spells.dragonbreath import DragonBreath
from game.spells.earthwall import EarthWall
from game.spells.explosion import Explosion
from game.spells.fallingmountains import FallingMountains
from game.spells.fireball import Fireball
from game.spells.firebody import FireBody
from game.spells.firewall import Firewall
from game.spells.footsteps import Footsteps
from game.spells.freeze import Freeze
from game.spells.heatpuff import HeatPuff
from game.spells.phoenixflames import PhoenixFlames
from game.spells.rocket import Rocket
from game.spells.sandstorm import Sandstorm
from game.spells.shield import Shield
from game.spells.swordofdestruction import SwordOfDestruction
from game.spells.water import Water
from game.spells.waterblast import WaterBlast
from game.spells.waterdart import WaterDart
from game.spells.watersembrace import WatersEmbrace
from game.spells.waterspikes import WaterSpikes
from game.spells.whirlpool import Whirlpool


class SpellCreator:
    def __init__(self, gameManager):
        self.element = None
        self.selected = 0
        self.gameManager = gameManager
        self.spellManager = self.gameManager.spellManager

    def updateElementAndSelected(self, element, selected):
        self.element = element
        self.selected = selected

    def tick(self, spellRegister):
        player = self.gameManager.playerManager.getMyPlayer()
        isometricRenderer = self.spellManager.isometricRenderer
        if self.element is not None:
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

                if self.selected == 6:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, DragonBreath):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 3:
                                add = False


                    if add:
                        placeX = math.floor(player.x)
                        placeY = math.floor(player.y)
                        placeZ = math.floor(player.z)
                        if player.direction == "n":
                            for i in range(3):
                                self.spellManager.addSpell(DragonBreath(placeX-(3-i), placeY-i, placeZ, player))
                                self.spellManager.addSpell(DragonBreath(placeX+(3-i), placeY-i, placeZ, player))

                        if player.direction == "s":
                            for i in range(3):
                                self.spellManager.addSpell(DragonBreath(placeX-(3-i), placeY+i, placeZ, player))
                                self.spellManager.addSpell(DragonBreath(placeX+(3-i), placeY+i, placeZ, player))

                        if player.direction == "e":
                            for i in range(3):
                                self.spellManager.addSpell(DragonBreath(placeX+i, placeY-(3-i), placeZ, player))
                                self.spellManager.addSpell(DragonBreath(placeX+i, placeY+(3-i), placeZ, player))

                        if player.direction == "w":
                            for i in range(3):
                                self.spellManager.addSpell(DragonBreath(placeX-i, placeY-(3-i), placeZ, player))
                                self.spellManager.addSpell(DragonBreath(placeX-i, placeY+(3-i), placeZ, player))

                    self.element = None

                if self.selected == 7:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, SwordOfDestruction):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 2:
                                add = False

                    if add:
                        self.spellManager.addSpell(SwordOfDestruction(player, self))

                    self.element = None

            elif self.element == "water":
                if self.selected == 0:
                    self.spellManager.addSpell(Freeze(player))
                    self.element = None

                if self.selected == 1:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                                         self.spellManager.isometricRenderer)
                        placeX = math.floor(targetX)
                        placeY = math.floor(targetY)
                        for j in range(-1, 2):
                            for i in range(-1, 2):
                                self.spellManager.addSpell(WaterSpikes(placeX+i, placeY+j, math.floor(player.z)-1, player.uuid))
                        self.element = None

                if self.selected == 2:
                    self.spellManager.addSpell(WaterDart(player))
                    self.element = None

                if self.selected == 3:
                    self.spellManager.addSpell(WaterBlast(player))
                    self.element = None

                if self.selected == 4:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, WatersEmbrace):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 1:
                                add = False

                    if add:
                        self.spellManager.addSpell(WatersEmbrace(player))

                    self.element = None

                if self.selected == 5:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, Whirlpool):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 1:
                                add = False

                    if add:
                        for r in range(1, 5):
                            for i in range(6):
                                self.spellManager.addSpell(Whirlpool(player, r, i*60+r*60/4))

                    self.element = None

                if self.selected == 6:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                                         self.spellManager.isometricRenderer)
                        dY = targetY - player.y
                        dX = targetX - player.x
                        dir = math.atan2(dY, dX)
                        self.spellManager.addSpell(Water(player.x, player.y, player, dir, self))
                        self.element = None

                if self.selected == 7:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, DeadCalm):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 1:
                                add = False

                    if add:
                        added = set()
                        for r in range(5):
                            for i in range(0, 360, 20):
                                place = (math.floor(player.x + math.cos(math.radians(i)) * r), math.floor(player.y + math.sin(math.radians(i)) * r))
                                if place not in added:
                                    self.spellManager.addSpell(DeadCalm(player, *place))
                                    added.add(place)

                    self.element = None

            elif self.element == "ground":
                if self.selected == 0:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                                         self.spellManager.isometricRenderer)
                        placeX = math.floor(targetX)
                        placeY = math.floor(targetY)
                        self.spellManager.addSpell(Boomerang(player, (placeX, placeY)))
                        self.element = None

                if self.selected == 1:
                    if player.direction == "n":
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)-1, math.floor(player.y)-1, math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x), math.floor(player.y)-1, math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)+1, math.floor(player.y)-1, math.floor(player.z)-1, player.uuid))

                    elif player.direction == "s":
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)-1, math.floor(player.y)+1, math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x), math.floor(player.y)+1, math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)+1, math.floor(player.y)+1, math.floor(player.z)-1, player.uuid))

                    elif player.direction == "e":
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)+1, math.floor(player.y)-1, math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)+1, math.floor(player.y), math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)+1, math.floor(player.y)+1, math.floor(player.z)-1, player.uuid))

                    else:
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)-1, math.floor(player.y)-1, math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)-1, math.floor(player.y), math.floor(player.z)-1, player.uuid))
                        self.spellManager.addSpell(EarthWall(math.floor(player.x)-1, math.floor(player.y)+1, math.floor(player.z)-1, player.uuid))

                    self.element = None

                if self.selected == 2:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, Shield):
                            if entity.sender == player.uuid:
                                add = False

                    if add:
                        self.spellManager.addSpell(Shield(player))

                    self.element = None

                if self.selected == 3:
                    closestPlayer = None
                    for oPlayer in self.gameManager.playerManager.players.values():
                        if player.uuid != oPlayer.uuid:
                            if closestPlayer is None:
                                closestPlayer = oPlayer

                            else:
                                if tools.dist(oPlayer.x, oPlayer.y, player.x, player.y) < tools.dist(closestPlayer.x, closestPlayer.y, player.x, player.y):
                                    closestPlayer = oPlayer

                    if closestPlayer is not None:
                        dir = math.atan2(closestPlayer.y - player.y, closestPlayer.x - player.x)
                        for i in range(3):
                            placeX = player.x + math.cos(dir) * i
                            placeY = player.y + math.sin(dir) * i
                            self.spellManager.addSpell(Footsteps(placeX, placeY, len(self.spellManager.isometricRenderer.map.data[round(placeY)][round(placeX)]), -dir, player.uuid))

                    self.element = None

                if self.selected == 4:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                                         self.spellManager.isometricRenderer)
                        dY = targetY - player.y
                        dX = targetX - player.x
                        dir = math.atan2(dY, dX)
                        self.spellManager.addSpell(Boulder(player, dir-math.pi/6))
                        self.spellManager.addSpell(Boulder(player, dir))
                        self.spellManager.addSpell(Boulder(player, dir+math.pi/6))
                        self.element = None

                if self.selected == 5:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, Rocket):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 2:
                                add = False

                    if add:
                        self.spellManager.addSpell(Rocket(player))

                    self.element = None

                if self.selected == 6:
                    if not spellRegister.ready:
                        targetX, targetY, _ = spellRegister.findPosition(*spellRegister.secondaryInfo[0],
                                                                         self.spellManager.isometricRenderer)
                        placeX = math.floor(targetX)
                        placeY = math.floor(targetY)
                        for j in range(-1, 2):
                            for i in range(-1, 2):
                                try:
                                    self.spellManager.addSpell(FallingMountains(placeX+i, placeY+j, len(self.spellManager.isometricRenderer.map.data[round(placeY+i)][round(placeX+j)])+3, player))

                                except IndexError:
                                    pass
                        self.element = None

                if self.selected == 7:
                    add = True
                    for entity in isometricRenderer.entities:
                        if isinstance(entity, Sandstorm):
                            if tools.dist(entity.x, entity.y, player.x, player.y) < 2:
                                add = False

                    if add:
                        for oY in range(-7, 8):
                            for oX in range(-7, 8):
                                self.spellManager.addSpell(Sandstorm(math.floor(player.x)+oX, math.floor(player.y)+oY, player))

                    self.element = None

