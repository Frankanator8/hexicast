import sys
import pygame
import math

from game.player import Player
from render.camera import Camera
from spells.spellidentifier import SpellIdentifier
from render.IsometricRenderer import IsometricRenderer
from render.IsometricMap import IsometricMap

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("gam")

IsometricRenderer.init()

clock = pygame.time.Clock()

spellID = SpellIdentifier()
camera = Camera(0, 0, screen)
iRenderer = IsometricRenderer(screen, camera)
map = IsometricMap("assets/map.txt")
player = Player(0, 0, 2, 1)
iRenderer.addEntity(player)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    mouseClicked = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    keys = pygame.key.get_pressed()
    dt = clock.get_time() / 1000 # sec

    player.tickKeys(keys, dt)
    camera.follow(player)
    spellID.tickMouse(mousePos, mouseClicked)

    spellID.updateSequence(screen)

    iRenderer.render(map)
    spellID.render(screen, dt)

    clock.tick(60)
    pygame.display.flip()

pygame.quit()
quit()
sys.exit()
