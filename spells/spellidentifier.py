import math

import pygame

import loader


class SpellIdentifier:
    FIRE_SPELLS = [
        [3, 4],
        [5, 4],
        [5, 4, 2],
        [3, 4, 5, 2],
        [5, 4, 6, 2],
        [3, 5, 2, 6],
        [5, 2, 3, 1, 4, 6],
        [3, 4, 5, 2, 4, 6],
    ]

    WATER_SPELLS = [
        [1, 2],
        [3, 4],
        [1, 2, 3],
        [1, 2, 3, 4],
        [1, 2, 4, 3, 5],
        [5, 4, 3, 2, 1],
        [2, 1, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
    ]

    GROUND_SPELLS = [
        [1, 2],
        [3, 4],
        [1, 2, 3],
        [1, 2, 3, 4],
        [1, 2, 4, 3, 5],
        [5, 4, 3, 2, 1],
        [2, 1, 4, 5, 6],
        [1, 2, 3, 4, 5, 6],
    ]

    def __init__(self, spellRegister):
        self.spellRegister = spellRegister
        self.possible = []
        self.degreeRotation = 0

    def render(self, screen):
        if self.spellRegister.locked:
            surf = pygame.Surface((screen.get_width(), screen.get_height()))
            surf.set_alpha(round(170+85*math.sin(math.radians(self.degreeRotation*8))))
            surf.fill((255, 255, 255, 0))
            element = self.spellRegister.sequence[1]
            if element == 1:
                element = "fire"
                lis = self.FIRE_SPELLS

            elif element == 3:
                element = "water"
                lis = self.WATER_SPELLS

            else:
                element = "ground"
                lis = self.GROUND_SPELLS

            for index, i in enumerate(self.possible):
                size = self.spellRegister.radius*0.8
                r = self.spellRegister.radius * 1.5
                img = loader.load_image(f"{element}E/{i}", size=(size, size))
                deg = 90 - self.degreeRotation - index * 360/len(self.possible)
                if deg < 0:
                    deg += 360
                rad = math.radians(deg)
                surf.blit(img, (self.spellRegister.center[0] + math.cos(rad)*r-size/2,
                                  self.spellRegister.center[1] - math.sin(rad)*r-size/2))

                idToDegree = {
                    1:90,
                    2:30,
                    3:330,
                    4:270,
                    5:210,
                    6:150
                }
                for j in range(1, len(lis[i])):
                    if j == 1:
                        color = (0, 0, 255)

                    else:
                        color = (0, 0, 0)
                    degPrev = math.radians(idToDegree[lis[i][j-1]])
                    degNow = math.radians(idToDegree[lis[i][j]])
                    prevX = self.spellRegister.center[0] + math.cos(rad)*r + math.cos(degPrev) * size/2.2
                    nowX =self.spellRegister.center[0] + math.cos(rad)*r + math.cos(degNow) * size/2.2
                    prevY = self.spellRegister.center[1] - math.sin(rad)*r - math.sin(degPrev) * size/2.2
                    nowY = self.spellRegister.center[1] - math.sin(rad)*r - math.sin(degNow) * size/2.2
                    pygame.draw.line(surf, color, (prevX, prevY), (nowX, nowY), width=round(size/12))
                    pygame.draw.circle(surf, color, (nowX, nowY), round(size/24))

            screen.blit(surf, (0, 0))

    def tick(self, dt):
        if self.spellRegister.locked:
            self.degreeRotation += 360/10 * dt
            self.degreeRotation %= 360
            element = self.spellRegister.sequence[1]
            if element == 1:
                element = self.FIRE_SPELLS

            elif element == 3:
                element = self.WATER_SPELLS

            else:
                element = self.GROUND_SPELLS

            specificSeq = self.spellRegister.sequence[3:]
            self.possible = []
            for index, pos in enumerate(element):
                good = True
                for i in range(len(specificSeq)):
                    if i >= len(pos):
                        good = False
                        break

                    if specificSeq[i] != pos[i]:
                        good = False

                if good:
                    self.possible.append(index)

        else:
            self.possible = []
            self.degreeRotation = 0
