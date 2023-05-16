import sys
import pygame
import math
from spells.spellidentifier import SpellIdentifier

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("gam")

clock = pygame.time.Clock()

spellID = SpellIdentifier()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    mouseClicked = pygame.mouse.get_pressed()
    mousePos = pygame.mouse.get_pos()
    dt = clock.get_time() / 1000 # sec

    spellID.tickMouse(mousePos, mouseClicked)
    spellID.render(screen, dt)
    spellID.updateSequence(screen)
    clock.tick(60)
    pygame.display.flip()

pygame.quit()
quit()
sys.exit()
