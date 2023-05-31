import random
import sys
import pygame

import loader
from audio.musicmaster import MusicMaster
from game.gameManager import GameManager
from game.map import Map
from game.player import Player
from game.playermanager import PlayerManager
from game.spellManager import SpellManager
from networking.gameNetworking import GameNetworking
from render.GuiRenderer import GuiRenderer
from render.camera import Camera
from render.fonts import Fonts
from render.gui.GameButton import GameButton
from render.gui.base.text import Text
from render.guiMaker import GuiMaker
from render.screenmaster import ScreenMaster
from spells.spellcreator import SpellCreator
from spells.spellidentifier import SpellIdentifier
from spells.spellregister import SpellRegister
from render.IsometricRenderer import IsometricRenderer
from render.IsometricMap import IsometricMap
import uuid as UUID

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hexicast")

IsometricRenderer.init()
Fonts.init()

clock = pygame.time.Clock()

gameNetworking = GameNetworking()

gameNetworking.loopGetGames()
gameNetworking.loopGameState()
gameNetworking.loopUpdateGame()


screenMaster = ScreenMaster()
camera = Camera(0, 0, screen)
iRenderer = IsometricRenderer(screen, camera)
iMap = IsometricMap("assets/better.txt")
map = Map(iMap)
iRenderer.setMap(iMap)

spellRe = SpellRegister()
spellId = SpellIdentifier(spellRe)
spellManager = SpellManager(iRenderer)
spellCreator = SpellCreator(spellManager)

playerManager = PlayerManager(gameNetworking, map, iRenderer)
gameManager = GameManager(playerManager, spellManager, gameNetworking, screenMaster)


guiRenderer = GuiRenderer(screen)
guiMaker = GuiMaker(screen, guiRenderer, gameNetworking, screenMaster, gameManager)
guiMaker.makeInitialGui()
previousGameList = []

screenMaster.addScreenFunc(0, guiMaker.updateScreen0)
screenMaster.addChangeFunc(1, guiMaker.on_login_window)
screenMaster.addScreenFunc(1, guiMaker.updateScreen1)
screenMaster.addChangeFunc(2, guiMaker.on_loading_window)
screenMaster.addScreenFunc(2, guiMaker.updateScreen2)

musicMaster = MusicMaster()

running = True
bg = loader.load_image("bg", size=(SCREEN_WIDTH, SCREEN_HEIGHT))
prevKeys = pygame.key.get_pressed()
prevClicked = pygame.mouse.get_pressed()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    mouseClicked = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    dt = clock.get_time() / 1000 # sec

    musicMaster.tick(dt)

    if 0 <= screenMaster.screenID < 10:
        musicMaster.playMusic("dvorak.mp3")
        guiRenderer.tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        guiRenderer.render(screen)

    if screenMaster.screenID == 10:
        screen.blit(bg, (0, 0))
        playerManager.tick(keys, prevKeys, dt)
        camera.follow(playerManager.getMyPlayer())
        spellRe.tickMouse(mousePos, mouseClicked, prevClicked)
        spellRe.updateSequence(screen)
        spellId.tick(dt, spellCreator)
        spellCreator.tick(playerManager.getMyPlayer(), spellRe, iRenderer)
        spellManager.tick(gameNetworking, dt)
        if gameNetworking.sendUuid == gameNetworking.lastSentUuid:
            gameNetworking.sendGameData = gameManager.updateGameData()
            gameManager.flush()
            gameNetworking.sendUuid = UUID.uuid4()

        iRenderer.render()
        spellRe.render(screen, dt)
        spellId.render(screen)

    # Text(f"{round(player.x)}, {round(player.y)}, {round(player.z)}", ("Calibri", 15), (0, 0, 0), (0, 0)).render(screen)

    clock.tick(60)
    screenMaster.tick()
    pygame.display.flip()
    prevKeys = keys
    prevClicked = mouseClicked

pygame.quit()
gameNetworking.close()
sys.exit()
