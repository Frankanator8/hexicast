import random
import sys
import pygame
import loader
from audio.musicmaster import MusicMaster
from audio.soundmaster import SoundMaster
from game.gameManager import GameManager
from game.map import Map
from game.playermanager import PlayerManager
from game.spellManager import SpellManager
from game.gameStateManager import GameStateManager
from networking.gameNetworking import GameNetworking
from render.GuiRenderer import GuiRenderer
from render.camera import Camera
from render.fonts import Fonts
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
musicMaster = MusicMaster()
soundMaster = SoundMaster()

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
gameStateManager = GameStateManager(gameNetworking, screenMaster)
gameManager = GameManager(playerManager, spellManager, gameNetworking, screenMaster, gameStateManager)


guiRenderer = GuiRenderer(screen)
guiMaker = GuiMaker(screen, guiRenderer, gameNetworking, screenMaster, gameManager, musicMaster, soundMaster)
guiMaker.makeInitialGui()
previousGameList = []

screenMaster.addScreenFunc(0, guiMaker.updateScreen0)
screenMaster.addChangeFunc(1, guiMaker.on_login_window)
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
        musicMaster.playMusic("demonslayer.mp3")
        guiRenderer.tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        guiRenderer.render(screen)

    if screenMaster.screenID == 10:
        musicMaster.playMusic("genshin.mp3")
        screen.blit(bg, (0, 0))
        playerManager.tick(keys, prevKeys, dt)
        if playerManager.getMyPlayer().alive:
            camera.follow(playerManager.getMyPlayer())

        else:
            camera.tickKeys(dt, keys, map)

        if playerManager.getMyPlayer().alive and not gameStateManager.gracePeriod:
            spellRe.tickMouse(mousePos, mouseClicked, prevClicked)
            spellRe.updateSequence(screen)
            spellId.tick(dt, spellCreator)
            spellCreator.tick(playerManager.getMyPlayer(), spellRe, iRenderer)
        spellManager.tick(gameNetworking, dt)
        gameStateManager.tick(dt, playerManager.getMyPlayer())
        if gameNetworking.sendUuid == gameNetworking.lastSentUuid:
            gameNetworking.sendGameData = gameManager.updateGameData()
            gameManager.flush()
            gameNetworking.sendUuid = UUID.uuid4()

        iRenderer.render()
        spellRe.render(screen, dt)
        spellId.render(screen)
        gameStateManager.render(screen)

    clock.tick(60)
    screenMaster.tick()
    pygame.display.flip()
    prevKeys = keys
    prevClicked = mouseClicked

pygame.quit()
gameNetworking.close()
sys.exit()
