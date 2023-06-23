import pygame

import loader
from game.map import Map
from render.IsometricMap import IsometricMap
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable
from render.miniIRenderer import MiniIsometricRenderer


class MapViewer(GuiElement):
    def __init__(self, x, y, w, h):
        self.renderSurf = pygame.Surface((w, h), pygame.SRCALPHA)
        self.miniIsometricRenderer = MiniIsometricRenderer(self.renderSurf, IsometricMap("", load=False))
        super().__init__(x, y, [Renderable(self.renderSurf, (x, y))])

    def setMapData(self, data):
        self.renderSurf.blit(loader.load_image("bg", size=self.renderSurf.get_size()), (0, 0))
        self.miniIsometricRenderer.map.load(data)
        self.miniIsometricRenderer.render()