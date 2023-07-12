import sys
import uuid as UUID
import os

from render.gui.base.text import Text
from render.miniIRenderer import MiniIsometricRenderer
import pygame
import loader
from audio.musicmaster import MusicMaster
from audio.soundmaster import SoundMaster
from game.gameManager import GameManager
from game.gameStateManager import GameStateManager
from game.map import Map
from game.playermanager import PlayerManager
from game.spellManager import SpellManager
from networking.gameNetworking import GameNetworking
from render.GuiRenderer import GuiRenderer
from render.IsometricMap import IsometricMap
from render.IsometricRenderer import IsometricRenderer
from render.camera import Camera
from render.fonts import Fonts
from render.guiMaker import GuiMaker
from render.screenmaster import ScreenMaster
from spells.spellcreator import SpellCreator
from spells.spellidentifier import SpellIdentifier
from spells.spellregister import SpellRegister
from game.decorManager import DecorManager

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_icon(loader.load_image("icon"))
pygame.display.set_caption("Hexicast")

pygame.event.set_allowed([pygame.QUIT])


IsometricRenderer.init()
MiniIsometricRenderer.init()
Fonts.init()
musicMaster = MusicMaster()
soundMaster = SoundMaster()

clock = pygame.time.Clock()

gameNetworking = GameNetworking()

gameNetworking.loopGetGames()
gameNetworking.loopGameState()
gameNetworking.loopUpdateGame()
gameNetworking.getMapInfo()
gameNetworking.loopUpdatePlayers()


screenMaster = ScreenMaster()
camera = Camera(0, 0, screen)
iRenderer = IsometricRenderer(screen, camera)
iMap = IsometricMap("assets/better.txt")
map = Map(iMap)
iRenderer.setMap(iMap)
spellManager = SpellManager(iRenderer)
decorManager = DecorManager(gameNetworking, iRenderer)
playerManager = PlayerManager(gameNetworking, map, iRenderer)
gameStateManager = GameStateManager(gameNetworking, screenMaster, screen)
gameManager = GameManager(playerManager, spellManager, gameNetworking, screenMaster, gameStateManager, decorManager)

spellRe = SpellRegister()
spellId = SpellIdentifier(spellRe)
spellCreator = SpellCreator(gameManager)


guiRenderer = GuiRenderer(screen)
guiMaker = GuiMaker(screen, guiRenderer, gameNetworking, screenMaster, gameManager, musicMaster, soundMaster)
guiMaker.makeInitialGui()
previousGameList = []

screenMaster.addScreenFunc(0, guiMaker.updateScreen0)
screenMaster.addChangeFunc(1, guiMaker.on_game_select_window)
screenMaster.addScreenFunc(1, guiMaker.updateScreen1)
screenMaster.addChangeFunc(2, guiMaker.on_loading_window)
screenMaster.addScreenFunc(2, guiMaker.updateScreen2)
screenMaster.addChangeFunc(3, guiMaker.on_end_screen)
screenMaster.addScreenFunc(3, guiMaker.updateScreen3)

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
        musicMaster.playMusic("Lobby_Music.wav")
        guiMaker.dt = dt
        guiRenderer.tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        guiRenderer.render(screen)

    if screenMaster.screenID == 10:
        musicMaster.playMusic("game1.wav")
        screen.blit(bg, (0, 0))
        playerManager.tick(keys, prevKeys, dt, gameManager.ticksSinceLastUpdate)
        if playerManager.getMyPlayer().alive:
            camera.follow(playerManager.getMyPlayer())

        else:
            camera.tickKeys(dt, keys, map)

        if playerManager.getMyPlayer().alive and not gameStateManager.gracePeriod:
            spellRe.tickMouse(mousePos, mouseClicked, prevClicked)
            spellRe.updateSequence()
            spellId.tick(dt, spellCreator)
            spellCreator.tick(spellRe)
        spellManager.tick(gameNetworking, dt, gameManager.ticksSinceLastUpdate)
        decorManager.tick(playerManager.getMyPlayer(), dt)
        gameStateManager.tick(dt, playerManager.getMyPlayer())
        if gameNetworking.sendUuid == gameNetworking.lastSentUuid:
            gameNetworking.sendGameData = gameManager.updateGameData()
            gameManager.flush()
            gameNetworking.sendUuid = UUID.uuid4()

        else:
            gameManager.ticks += 1

        iRenderer.doAnimationTick(dt)
        iRenderer.render()
        spellRe.render(screen, dt)
        spellId.render(screen)
        gameStateManager.render(screen)
    Text(f"FPS {round(clock.get_fps())}", ("Calibri", 15), (0, 0, 0), (0, 0)).render(screen)
    clock.tick(60)
    screenMaster.tick()
    pygame.display.flip()
    prevKeys = keys
    prevClicked = mouseClicked

pygame.quit()
gameNetworking.close()
sys.exit()
