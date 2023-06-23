import math
import tools
import pygame

import loader

class MiniIsometricRenderer:
    WATER = None
    GRASS = None
    STONE = None
    SAND = None
    TILE_SIZE = (4, 4)
    @classmethod
    def init(cls):
        cls.GRASS = loader.load_image("map/grass", size=cls.TILE_SIZE)
        cls.WATER = loader.load_image("map/water", size=cls.TILE_SIZE)
        cls.STONE = loader.load_image("map/stone", size=cls.TILE_SIZE)
        cls.SAND = loader.load_image("map/sand", size=cls.TILE_SIZE)
        cls.BLOCK_DICT = {
            0:cls.WATER,
            1:cls.GRASS,
            2:cls.STONE,
            3:cls.SAND
        }
        cls.TINT_DEGREE = {
            0:180,
            1:205,
            3:230,
            4:240,
            5:255
        }
    def __init__(self, screen, map):
        self.screen = screen
        self.map = map
        self.renderShadows = True
        self.renderCache = {}

    def getIsoXY(self, x, y, z, display):
        size = self.TILE_SIZE
        cart_x = x * size[0]/2
        cart_y = y * size[1]/2
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2.153 - z * size[1]*0.5

        iso_x += display.get_width()/2
        iso_y += display.get_height()/4
        return iso_x, iso_y

    def is_visible(self, x, y, z):
        good = False
        try:
            self.map.data[y+1][x][z]

        except IndexError:
            good = True

        try:
            self.map.data[y][x+1][z]

        except IndexError:
            good = True

        try:
            self.map.data[y][x][z+1]

        except IndexError:
            good = True


        return good

    def getTint(self, x, y, z):
        try:
            tintDegree = self.TINT_DEGREE[z]

        except KeyError:
            tintDegree = 255

        if z < self.map.shadowMap[y][x]:
            if self.renderShadows:
                tintDegree -= 70

        return tintDegree

    def render(self):
        map = self.map
        display = self.screen
        size = self.TILE_SIZE

        for y, row in enumerate(map.data):
            for x, cell in enumerate(row):
                for z, block in enumerate(cell):
                    if self.is_visible(x, y, z):
                        iso_x, iso_y = self.getIsoXY(x, y, z, display)
                        if not (iso_x+size[0] < 0 or iso_x > display.get_width() or iso_y+size[1] < 0 or iso_y > display.get_height()):
                            tintDegree = self.getTint(x, y, z)
                            if (block, tintDegree) not in self.renderCache.keys():
                                tex = self.BLOCK_DICT[block].copy()
                                tex.fill((tintDegree, tintDegree, tintDegree), None, pygame.BLEND_RGBA_MULT)
                                self.renderCache[(block, tintDegree)] = tex

                            else:
                                tex = self.renderCache[(block, tintDegree)]

                            display.blit(tex, (iso_x, iso_y))
