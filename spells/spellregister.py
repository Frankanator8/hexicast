import math
import random

import pygame.draw

import loader
from audio.soundlibrary import SoundLibrary
from tools import dist
from spells.polygon import generate_polygon


class SpellRegister:
    soundMaster = None
    EMBLEM_R_MULTIPLIER = 3
    def __init__(self):
        self.trail = []
        self.sequence = []
        self.ready = False
        self.locked = False
        self.center = (0, 0)
        self.radius = 0
        self.particles = []
        self.emblem = None
        self.secondaryInfo = [(0, 0), (0, 0)]
        self.lastPoint = (0, 0)

        self.spellSoundUuid = ""

    @staticmethod
    def findPosition(x, y, isometricRenderer):
        return isometricRenderer.getXYZ(x, y, precise=True)

    def findLastPosition(self, isometricRenderer, screen):
        return self.findPosition(*self.secondaryInfo[-1], isometricRenderer, screen)

    def tickMouse(self, mousePos, mousePressed, prevPressed):
        if mousePressed[0]:
            if not self.locked:
                if not prevPressed[0]:
                    self.secondaryInfo = (mousePos, self.lastPoint)
            self.trail.append(mousePos)
            self.ready = False

        else:
            self.ready = True
            self.locked = False
            self.trail = []

    def render(self, screen, dt):
        iToID = {
            0:2,
            1:1,
            2:6,
            3:5,
            4:4,
            5:3
        }
        if self.locked:
            surf = pygame.Surface((screen.get_width(), screen.get_height()), flags=pygame.SRCALPHA)
            surf.set_alpha(100)
            surf.fill((255, 255, 255, 0))
            if self.sequence[1] == 1: # Fire
                if not self.soundMaster.isPlaying(self.spellSoundUuid):
                    self.spellSoundUuid = self.soundMaster.playSound(SoundLibrary.FIRE)

                if len(self.particles) < round(self.radius * 2):
                    for i in range(round(self.radius * 2)-len(self.particles)):
                        r = random.randint(200, 255)
                        self.particles.append([(r, random.randint(0, round(0.7*r)), 0), random.randint(10, 50),
                                               [round(self.center[0] + random.randint(-round(self.radius), round(self.radius))),
                                                round(self.center[1]) - random.randint(round(self.radius*0.3), round(self.radius))],
                                               random.randint(100, 200)])

                newParticles = []
                for i in self.particles:
                    pygame.draw.circle(surf, i[0], i[2], i[1])
                    i[1] -= dt*30
                    i[2][1] -= i[3] * dt
                    if i[1] > 0:
                        newParticles.append(i)

                self.particles = newParticles

            elif self.sequence[1] == 3: # water
                if not self.soundMaster.isPlaying(self.spellSoundUuid):
                    self.spellSoundUuid = self.soundMaster.playSound(SoundLibrary.WATER)
                if len(self.particles) < 400:
                    for i in range(400 - len(self.particles)):
                        side = -1
                        if random.randint(1, 2) == 1:
                            side = 1

                        rg = random.randint(0, 255)
                        self.particles.append([(rg, rg, 255), random.randint(10, 20),
                                               [round(self.center[0] + side*random.uniform(0, 1) * self.radius), self.center[1]], side,
                                               random.randint(0, 10)])

                newParticles = []
                for i in self.particles:
                    pygame.draw.circle(surf, i[0], i[2], i[1])
                    i[2][1] += 1.7**((i[2][1]/screen.get_height()+1) * 7) * dt
                    i[2][0] += i[3] * 10*dt * i[4]
                    if i[2][1] < screen.get_width():
                        if random.randint(1, 40) != 1:
                                newParticles.append(i)

                self.particles = newParticles

            elif self.sequence[1] == 5: # Ground
                if not self.soundMaster.isPlaying(self.spellSoundUuid):
                    self.spellSoundUuid = self.soundMaster.playSound(SoundLibrary.GROUND)
                if len(self.particles) < 10:
                    for i in range(10 - len(self.particles)):
                        y = self.center[1] + random.uniform(0, self.radius)
                        poly = generate_polygon((self.center[0] + random.uniform(-1, 1) * self.radius, y),
                                            30, 0.8, random.uniform(0, 0.5), random.randint(6, 10))
                        self.particles.append([poly, (random.randint(133, 209), 209, 93), 0,  y])

                newParticles = []
                for i in self.particles:
                    pygame.draw.polygon(surf, i[1], i[0])
                    oldY = i[3]
                    i[3] += 1.7**((i[3]/screen.get_height()+1) * 7) * dt

                    diff = i[3] - oldY

                    for j in i[0]:
                        j[1] += diff


                    if i[3] < screen.get_width():
                        if random.randint(1, 40) != 1:
                            newParticles.append(i)

                self.particles = newParticles


            screen.blit(surf, (0, 0))
            screen.blit(self.emblem, (self.center[0] - self.radius*self.EMBLEM_R_MULTIPLIER/2, self.center[1] - self.radius*self.EMBLEM_R_MULTIPLIER/2))

            for i in range(6):
                if self.sequence.count(iToID[i]) == 0:
                    color = (255, 0, 0)

                elif self.sequence[-1] == iToID[i]:
                    color = (255, 255, 0)

                else:
                    gValue = 255 * self.sequence.count(iToID[i])/len(self.sequence)*4
                    if gValue > 255:
                        gValue = 255
                    color = (0, gValue, 0)
                pygame.draw.circle(screen, color, (self.center[0]+self.radius*math.cos(i*math.pi/3+math.pi/6), self.center[1]-self.radius*math.sin(i*math.pi/3+math.pi/6)), self.radius/10)
        else:
            self.particles = []

        surf = pygame.Surface((screen.get_width(),screen.get_height()), flags=pygame.SRCALPHA)
        surf.set_alpha(100)
        surf.fill((255, 255, 255, 0))
        if len(self.trail) >= 2:
            for i in range(1, len(self.trail)):
                pygame.draw.line(surf, (0, 255, 255), self.trail[i-1], self.trail[i],
                                 width=round(5+(i/len(self.trail))*10))
                pygame.draw.circle(surf, (0, 255, 255), self.trail[i], round((5+(i/len(self.trail))*10)/2))

        screen.blit(surf, (0, 0))

    @staticmethod
    def getClosest30(ang):
        minAngle = 0
        for i in range(0, 360, 30):
            if abs(ang - i) < abs(ang - minAngle):
                minAngle = i

        return minAngle
    @staticmethod
    def diffAng(ang1, ang2):
        a = ang1 - ang2
        if a>180:
            a-=360

        if a < -180:
            a += 360

        return abs(a)
    def setInPlace(self, ang1, ang2, pt):
        if ang1 > 180:
            ang1 -= 180

        ang1 = self.getClosest30(ang1)
        ang2 = self.getClosest30(ang2)
        top = [(30, 330), (150, 210)]
        left = [(90, 330), (150, 90)]
        right = [(90, 210), (30, 90)]
        aPair = (ang1, ang2)
        self.sequence = []
        if aPair == top[0]:
            self.sequence = [6, 1, 2]

        if aPair == top[1]:
            self.sequence = [2, 1, 6]

        if aPair == left[0]:
            self.sequence = [6, 5, 4]

        if aPair == left[1]:
            self.sequence = [4, 5, 6]

        if aPair == right[0]:
            self.sequence = [2, 3, 4]

        if aPair == right[1]:
            self.sequence = [4, 3, 2]

        if len(self.sequence) != 0:
            self.locked = True
            self.radius = dist(*pt, *self.trail[0])
            if aPair in top:
                self.center = (pt[0], pt[1]+self.radius)

            elif aPair in left:
                self.center = (pt[0] + self.radius * math.cos(math.radians(30)),
                               pt[1] - self.radius * math.sin(math.radians(30)))

            elif aPair in right:
                self.center = (pt[0] - self.radius * math.cos(math.radians(30)),
                               pt[1] - self.radius * math.sin(math.radians(30)))

            self.emblem = loader.load_image("emblem", size=(self.radius*self.EMBLEM_R_MULTIPLIER, self.radius*self.EMBLEM_R_MULTIPLIER))



    def updateSequence(self):
        # Text(f"{self.sequence}", ("Calibri", 15), (255, 255, 255), (0, 0)).render(screen)
        if not self.locked:
            if len(self.trail) > 0:
                dOY = self.trail[0][1] - self.trail[-1][1]
                dOX = self.trail[-1][0] - self.trail[0][0]
                if dOX == 0:
                    dOX = 0.01

                oAng = math.degrees(math.atan2(dOY, dOX))
                if oAng < 0:
                    oAng += 360

            for i in range(len(self.trail)):
                before = self.trail[:i]
                after = self.trail[i:]
                if len(before) == 0 or len(after) == 0:
                    continue

                if abs(dist(*self.trail[0], *self.trail[i])-dist(*self.trail[-1], *self.trail[i]))>30:
                    continue

                dBY = before[-1][1] - before[0][1]
                dBX = before[0][0] - before[-1][0]
                if dBX == 0:
                    dBX = 0.01

                bAng = math.degrees(math.atan2(dBY, dBX))
                if bAng < 0:
                    bAng += 360

                dAY = after[0][1] - after[-1][1]
                dAX = after[-1][0] - after[0][0]
                if dAX == 0:
                    dAX = 0.01

                aAng = math.degrees(math.atan2(dAY, dAX))
                if aAng < 0:
                    aAng += 360

                if self.diffAng(oAng, bAng) < 10 or self.diffAng(oAng, aAng) < 10:
                    continue

                if 100 < self.diffAng(aAng, bAng) < 140:
                    self.setInPlace(bAng, aAng, self.trail[i])
                    break

        else:
            degreeToID = {
                90:1,
                30:2,
                330:3,
                270:4,
                210:5,
                150:6

            }
            for i in range(30, 360, 60):
                pt = (self.center[0] + self.radius * math.cos(math.radians(i)),
                      self.center[1] - self.radius * math.sin(math.radians(i)))
                if dist(*self.trail[-1], *pt) < self.radius/3:
                    if degreeToID[i] != self.sequence[-1]:
                        self.sequence.append(degreeToID[i])
            self.lastPoint = self.trail[-1]
