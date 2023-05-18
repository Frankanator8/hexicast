import sys
import pygame
import math

import loader
from game.player import Player
from render.camera import Camera
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
camera = Camera(0, 0, screen)
iRenderer = IsometricRenderer(screen, camera)
map = IsometricMap("assets/map.txt")
player = Player(0, 0, 2, 1)
iRenderer.addEntity(player)
running = True

bg = loader.load_image("bg", size=(SCREEN_WIDTH, SCREEN_HEIGHT))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))

    mouseClicked = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    dt = clock.get_time() / 1000 # sec

    player.tickKeys(keys, dt)
    camera.follow(player)
    spellRe.tickMouse(mousePos, mouseClicked)
    spellRe.updateSequence(screen)
    spellId.tick(dt)

    iRenderer.render(map)
    spellRe.render(screen, dt)
    spellId.render(screen)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
quit()
sys.exit()
