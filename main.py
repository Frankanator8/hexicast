import sys
import pygame

import loader
from game.map import Map
from game.player import Player
from networking.gameNetworking import GameNetworking
from render.GuiRenderer import GuiRenderer
from render.camera import Camera
from render.gui.GameButton import GameButton
from render.gui.base.text import Text
from render.guiMaker import makeGui
from render.screenmaster import ScreenMaster
from spells.spellidentifier import SpellIdentifier
from spells.spellregister import SpellRegister
from render.IsometricRenderer import IsometricRenderer
from render.IsometricMap import IsometricMap

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("gam")

IsometricRenderer.init()

clock = pygame.time.Clock()

spellRe = SpellRegister()
spellId = SpellIdentifier(spellRe)

gameNetworking = GameNetworking()
gameNetworking.loopGetGames()

screenMaster = ScreenMaster()
camera = Camera(0, 0, screen)
iRenderer = IsometricRenderer(screen, camera)
iMap = IsometricMap("assets/better.txt")
map = Map(iMap)
iRenderer.setMap(iMap)

font24 = (loader.load_font("theFont", 24), 24)
font48 = (loader.load_font("theFont", 48), 48)
guiRenderer = GuiRenderer(screen)
makeGui(guiRenderer, screen, gameNetworking, font48, font24)
previousGameList = []

player = Player(36, 36, 2, 1)
iRenderer.addEntity(player)
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

    if 0<= screenMaster.screenID < 10:
        guiRenderer.tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        guiRenderer.render(screen)

    if screenMaster.screenID == 0:
        if guiRenderer.get_element("nameInput").text == "":
            guiRenderer.get_element("submitName").show = False

        else:
            guiRenderer.get_element("submitName").show = True

        if gameNetworking.uuid != "":
            screenMaster.screenID = 1
            guiRenderer.get_element("nameInputBanner").show = False
            guiRenderer.get_element("nameInput").show = False
            guiRenderer.get_element("submitName").show = False
            guiRenderer.get_element("gameNameInput").show = True
            guiRenderer.get_element("lightBlueBanner").show = True
            guiRenderer.get_element("createBanner").show = True
            guiRenderer.get_element("nameBanner").show = True
            guiRenderer.get_element("playerCountInput").show = True
            guiRenderer.get_element("playerCountBanner").show = True
            guiRenderer.get_element("lobbySepLine").show = True

    elif screenMaster.screenID == 1:
        try:
            if guiRenderer.get_element("gameNameInput").text != "" and int(guiRenderer.get_element("playerCountInput").text) >= 2:
                guiRenderer.get_element("gameSubmit").show = True

            else:
                guiRenderer.get_element("gameSubmit").show = False

        except ValueError:
            guiRenderer.get_element("gameSubmit").show = False

        w=screen.get_width()*0.381966011
        for tag in previousGameList:
            guiRenderer.remove_element(tag)
        previousGameList = []
        for index, uuid in enumerate(gameNetworking.games.keys()):
            game = gameNetworking.games[uuid]
            print(game)
            thisButton = GameButton(w+10, 200+index*28, game, (116, 213, 255) if index%2==1 else (255, 255, 255), font24, screen.get_width())
            previousGameList.append(f"gameListButton{index}")
            guiRenderer.add_element(thisButton, tag=f"gameListButton{index}")

    if screenMaster.screenID == 10:
        screen.blit(bg, (0, 0))
        player.tickKeys(keys, prevKeys, dt, map)
        camera.follow(player)
        spellRe.tickMouse(mousePos, mouseClicked)
        spellRe.updateSequence(screen)
        spellId.tick(dt)

        iRenderer.render()
        spellRe.render(screen, dt)
        spellId.render(screen)
        Text(f"{round(player.x)}, {round(player.y)}, {round(player.z)}", ("Calibri", 15), (0, 0, 0), (0, 0)).render(screen)

    clock.tick(60)
    pygame.display.flip()
    prevKeys = keys
    prevClicked = mouseClicked


pygame.quit()
quit()
sys.exit()
