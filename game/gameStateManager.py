import math
import time
import random

import pygame

from render.fonts import Fonts
from render.gui.base.text import Text


class GameStateManager:
    def __init__(self, gameNetworking, screenMaster):
        self.gameNetworking = gameNetworking
        self.showGracePeriod = True
        self.showDeathScreen = False
        self.playerPos = (0, 0, 0)
        self.ticks = 0
        self.endGame = False
        self.endGameTime = 0
        self.screenMaster = screenMaster
        self.gracePeriod = False

    def reset(self):
        self.showGracePeriod = True
        self.showDeathScreen = False
        self.playerPos = (0, 0, 0)
        self.ticks = 0
        self.endGame = False
        self.endGameTime = 0
        self.gracePeriod = False

    @property
    def timeElapsed(self):
        return time.time() - self.gameNetworking.gameData["gameData"]["timeStart"]
    def tick(self, dt, player):
        if self.ticks > 0:
            if (player.x, player.y, player.z) != self.playerPos:
                self.showGracePeriod = False

        if self.timeElapsed < 1:
            self.gracePeriod = True

        else:
            self.gracePeriod = False

        self.playerPos = (player.x, player.y, player.z)
        self.ticks += 1
        self.showDeathScreen = not player.alive
        if len(self.gameNetworking.gameData["result"].keys()) + 1 >= len(self.gameNetworking.gameData["players"]):
            self.endGame = True

        if self.endGame:
            self.endGameTime += dt

        if self.endGameTime > 2.8:
            self.screenMaster.screenID = 3
            self.gameNetworking.gameUuid = ""
            self.endGame = False

    def render(self, screen):
        timeRenderer = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        timeRenderer.set_alpha(180)
        pygame.draw.polygon(timeRenderer, (0, 178, 222), [(0, 0), (70, 0), (50, 25), (0, 25)])
        secs = self.timeElapsed
        seconds = math.floor(secs%60)
        minutes = round(secs//60)
        if seconds < 10:
            timeText = f"{minutes}:0{seconds}"

        else:
            timeText = f"{minutes}:{seconds}"

        Text(timeText, Fonts.font24, (0, 0, 0), (5, 0)).render(timeRenderer)

        if self.gameNetworking.gameData["gameData"]["period"] == 0:
            periodText = "Grace Period"

        else:
            periodText = "Battle Period"

        periodTextObj = Text(periodText, Fonts.font24, (0, 0, 0), (75, 0))

        pygame.draw.polygon(timeRenderer, (255, 255, 255), [(70, 0), (70+periodTextObj.w+30, 0), (70+periodTextObj.w+10, 25), (50, 25)])
        periodTextObj.render(timeRenderer)

        screen.blit(timeRenderer, (0, 0))

        if self.timeElapsed < 27:
            if self.showGracePeriod:
                graceHelp = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
                graceHelp.set_alpha(230)
                points = []
                for i in range(30, 360, 60):
                    points.append((screen.get_width()/2+200*math.cos(math.radians(i)), screen.get_height()/2-200*math.sin(math.radians(i))))

                pygame.draw.polygon(graceHelp, (255, 255, 255), points)

                gracePeriodText = Text("Grace Period", Fonts.font48, (0, 0, 0), (0, 0))
                gracePeriodText.centerAt(screen.get_width()/2, screen.get_height()/2-90)
                gracePeriodText.render(graceHelp)
                graceHelpT = Text("During the grace period, you will NOT\nbe able to see other players.\n\nUse this time to go to where you want\nto start before the battle begins\nat 30 seconds",
                                 Fonts.font24, (0, 0, 0), (0, 0))
                graceHelpT.centerAt(screen.get_width()/2, screen.get_height()/2+10)
                graceHelpT.render(graceHelp)
                screen.blit(graceHelp, (0, 0))

        if 27 <= self.timeElapsed <= 30:
            degree = 1-self.timeElapsed%1
            timeText = Text(f"{math.ceil(30-self.timeElapsed)}", Fonts.font150, (255, 0, 0), (0, 0))
            countdownSurf = pygame.Surface((timeText.w, timeText.h), pygame.SRCALPHA)
            timeText.render(countdownSurf)
            countdownSurf.set_alpha(degree*255)
            countdownSurf = pygame.transform.scale(countdownSurf, ((4+3*(1-degree))*timeText.w, (4+3*(1-degree))*timeText.h))
            screen.blit(countdownSurf, (screen.get_width()/2-countdownSurf.get_width()/2, screen.get_height()/2-countdownSurf.get_height()/2))

        if 30 <= self.timeElapsed <= 32:
            degree = (32-self.timeElapsed)/2
            fightText = Text(f"F I G H T !", Fonts.font150, (255, 0, 0), (0, 0))
            fightSurf = pygame.Surface((fightText.w, fightText.h), pygame.SRCALPHA)
            fightText.render(fightSurf)
            fightSurf.set_alpha(degree*255)
            fightSurf = pygame.transform.scale(fightSurf, ((1+2*(1-degree))*fightText.w, (1+2*(1-degree))*fightText.h))
            screen.blit(fightSurf, (screen.get_width()/2-fightSurf.get_width()/2, screen.get_height()/2-fightSurf.get_height()/2))

        if self.showDeathScreen:
            redScreen = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            redScreen.fill((255, 0, 0))
            redScreen.set_alpha(round(100+math.sin(self.timeElapsed)*40))
            screen.blit(redScreen, (0, 0))
            deathText = Text("You died. You are now spectating the game.", Fonts.font48, (255, 255, 255), (0, 0))
            deathText.centerAt(screen.get_width()/2, screen.get_height()-80)
            deathText.render(screen)

        if self.endGame:
            leftInShift = (1-self.endGameTime)
            if leftInShift < 0:
                leftInShift = 0
            shift = random.randint(-10, 10) - leftInShift * screen.get_width()

            if leftInShift == 0:
                for i in range(random.randint(30, 60)):
                    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(screen.get_width()/2 + shift+random.randint(-300, 300),
                                                                          screen.get_height()/2 + shift+random.randint(-100, 100),
                                                                          10, 10))
            pygame.draw.polygon(screen, (0, 255, 0), [(screen.get_width()/2-280+shift, screen.get_height()/2-70),
                                                      (screen.get_width()/2+270+shift, screen.get_height()/2-70),
                                                      (screen.get_width()/2+300+shift, screen.get_height()/2+70),
                                                      (screen.get_width()/2-260+shift, screen.get_height()/2+70)])
            pygame.draw.polygon(screen, (255, 255, 255), [(screen.get_width()/2-240+shift, screen.get_height()/2-50),
                                                      (screen.get_width()/2+240+shift, screen.get_height()/2-50),
                                                      (screen.get_width()/2+260+shift, screen.get_height()/2+50),
                                                      (screen.get_width()/2-220+shift, screen.get_height()/2+50)])


            gameText = Text("G A M E !", Fonts.font150, (255, 0, 0), (0, 0))
            gameText.centerAt(screen.get_width()/2 + shift, screen.get_height()/2)
            gameText.render(screen)
