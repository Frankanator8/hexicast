import copy
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
        [1, 6],
        [6, 2, 4],
        [1, 6, 2],
        [1, 2, 5, 4],
        [5, 6, 2, 4],
        [5, 6, 4, 2, 5, 3],
        [1, 6, 5, 2, 6, 4],
        [5, 2, 6, 3, 1, 5],
    ]

    GROUND_SPELLS = [
        [2, 6],
        [3, 1, 6],
        [3, 2, 6],
        [3, 5, 1],
        [2, 1, 6, 3],
        [3, 6, 2, 4],
        [3, 2, 6, 3, 1, 5],
        [1, 3, 2, 6, 1, 5],
    ]

    def __init__(self, spellRegister):
        self.spellRegister = spellRegister
        self.possible = []
        self.degreeRotation = 0
        self.selected = None
        self.animationSelectTick = 0
        self.element = None

    def render(self, screen):
        if self.spellRegister.locked:
            self.animationSelectTick = 0
            surf = pygame.Surface((screen.get_width(), screen.get_height()), flags=pygame.SRCALPHA)
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
                use = copy.deepcopy(lis[i])
                use.insert(0, self.spellRegister.sequence[2])
                use = use[len(self.spellRegister.sequence)-3:]


                for j in range(1, len(use)):
                    if j == 1:
                        color = (0, 0, 255)

                    else:
                        color = (0, 0, 0)
                    degPrev = math.radians(idToDegree[use[j-1]])
                    degNow = math.radians(idToDegree[use[j]])
                    prevX = self.spellRegister.center[0] + math.cos(rad)*r + math.cos(degPrev) * size/2.2
                    nowX =self.spellRegister.center[0] + math.cos(rad)*r + math.cos(degNow) * size/2.2
                    prevY = self.spellRegister.center[1] - math.sin(rad)*r - math.sin(degPrev) * size/2.2
                    nowY = self.spellRegister.center[1] - math.sin(rad)*r - math.sin(degNow) * size/2.2
                    pygame.draw.line(surf, color, (prevX, prevY), (nowX, nowY), width=round(size/12))
                    pygame.draw.circle(surf, color, (nowX, nowY), round(size/24))


            screen.blit(surf, (0, 0))

        else:
            if self.selected is not None:
                if self.animationSelectTick < 1:
                    self.animationSelectTick *= 2
                    element = self.element

                    x = self.spellRegister.center[0] - (self.spellRegister.radius/2 + self.spellRegister.radius/2 * self.animationSelectTick)
                    y = self.spellRegister.center[1] - (self.spellRegister.radius/2 + self.spellRegister.radius/2 * self.animationSelectTick)
                    surf = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                    surf.set_alpha(200-200*self.animationSelectTick)
                    surf.blit(loader.load_image(f"{element}E/{self.selected}",
                                                size=((self.spellRegister.radius/2 + self.spellRegister.radius/2 * self.animationSelectTick)*2,
                                                      (self.spellRegister.radius/2 + self.spellRegister.radius/2 * self.animationSelectTick)*2)),
                              (x, y))
                    screen.blit(surf, (0, 0))
                    self.animationSelectTick /= 2


    def tick(self, dt, spellCreator):
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
            if len(self.possible) >= 1:
                element = self.spellRegister.sequence[1]
                if element == 1:
                    self.element = "fire"
                    lis = self.FIRE_SPELLS

                elif element == 3:
                    self.element = "water"
                    lis = self.WATER_SPELLS

                else:
                    self.element = "ground"
                    lis = self.GROUND_SPELLS

                self.selected = None
                for index, pos in enumerate(lis):
                    if pos == self.spellRegister.sequence[3:]:
                        self.selected = index
                        spellCreator.updateElementAndSelected(self.element, self.selected)
                        break

            else:
                if self.animationSelectTick == 0:
                    self.selected = None

            self.animationSelectTick += dt

            self.possible = []
            self.degreeRotation = 0
