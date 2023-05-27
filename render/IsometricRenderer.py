import math
import tools
import pygame

import loader


class IsometricRenderer:
    TILE_SIZE = (96, 96)
    @classmethod
    def init(cls):
        cls.GRASS = loader.load_image("map/grass", size=cls.TILE_SIZE)
        cls.WATER = loader.load_image("map/water", size=cls.TILE_SIZE)
        cls.STONE = loader.load_image("map/stone", size=cls.TILE_SIZE)
        cls.BLOCK_DICT = {
            0:cls.WATER,
            1:cls.GRASS,
            2:cls.STONE
        }
        cls.TINT_DEGREE = {
            0:180,
            1:205,
            3:230,
            4:240,
            5:255
        }
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.entities = []
        self.map = None
        self.renderShadows = True
        self.renderCache = {}
        self.renderPoses = {}

    def addEntity(self, entity):
        self.entities.append(entity)

    def removeEntity(self, entity):
        self.entities.remove(entity)

    def setMap(self, map):
        self.map = map

    def getIsoXY(self, x, y, z, display):
        size = self.TILE_SIZE
        cart_x = x * size[0]/2
        cart_y = y * size[1]/2
        iso_x = cart_x - cart_y
        iso_y = (cart_x + cart_y) / 2.153 - z * size[1]*0.5

        iso_x += display.get_width()/2
        iso_y += display.get_height()/2
        return iso_x, iso_y

    def getXYZ(self, x, y, display):
        possible = []
        for key, value in self.renderPoses.items():
            if y > key[0].getPointAt(x) and y > key[1].getPointAt(x) and y < key[2].getPointAt(x) and y < key[3].getPointAt(x):
                possible.append(value)

        if len(possible) > 0:
            ans = possible[0]
            for posAns in possible:
                if posAns[2] > ans[2]:
                    ans = posAns

            return ans

        return (0, 0, 0)

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
        camera = self.camera
        size = self.TILE_SIZE
        placeDicts = {}
        self.renderPoses = {}
        for entity in self.entities:
            if (math.floor(entity.x), math.floor(entity.y)) not in placeDicts.keys():
                placeDicts[(math.floor(entity.x), math.floor(entity.y))] = []
            placeDicts[(math.floor(entity.x), math.floor(entity.y))].append(entity)

        for y, row in enumerate(map.data):
            for x, cell in enumerate(row):
                for z, block in enumerate(cell):
                    oldY = y
                    oldX = x
                    x -= camera.x
                    y -= camera.y

                    iso_x, iso_y = self.getIsoXY(x, y, z, display)
                    if not (iso_x+size[0] < 0 or iso_x > display.get_width() or iso_y+size[1] < 0 or iso_y > display.get_height()):
                        tintDegree = self.getTint(oldX, oldY, z)
                        if ((block, tintDegree) not in self.renderCache.keys()):
                            tex = self.BLOCK_DICT[block].copy()
                            tex.fill((tintDegree, tintDegree, tintDegree), None, pygame.BLEND_RGBA_MULT)
                            self.renderCache[(block, tintDegree)] = tex

                        else:
                            tex = self.renderCache[(block, tintDegree)]

                        display.blit(tex, (iso_x, iso_y))
                        topPt = (iso_x + self.TILE_SIZE[0]/2, iso_y)
                        botPt = (iso_x + self.TILE_SIZE[0]/2, iso_y + self.TILE_SIZE[1]/2)
                        self.renderPoses[(tools.Line.determineFromSlopePoint(1/2, *topPt),
                                          tools.Line.determineFromSlopePoint(-1/2, *topPt),
                                          tools.Line.determineFromSlopePoint(1/2, *botPt),
                                          tools.Line.determineFromSlopePoint(-1/2, *botPt))] = (oldX, oldY, z)

                    y = oldY
                    x = oldX

                    if (x, y) in placeDicts.keys():
                        for entity in placeDicts[(x, y)]:
                            cameraX = entity.x - camera.x
                            cameraY = entity.y - camera.y
                            iso_x, iso_y = self.getIsoXY(cameraX, cameraY, (entity.z+1), display)
                            if not (iso_x+size[0] < 0 or iso_x > display.get_width() or iso_y+size[1] < 0 or iso_y > display.get_height()):
                                tintDegree = self.getTint(oldX, oldY, math.floor(z))
                                if ((f"{entity.image}/{entity.direction}", tintDegree) not in self.renderCache.keys()):
                                    tex = loader.load_image(f"{entity.image}/{entity.direction}", size=size)
                                    tex.fill((tintDegree, tintDegree, tintDegree), None, pygame.BLEND_RGBA_MULT)
                                    self.renderCache[(f"{entity.image}/{entity.direction}", tintDegree)] = tex

                                else:
                                    tex = self.renderCache[(f"{entity.image}/{entity.direction}", tintDegree)]

                                display.blit(tex, (iso_x, iso_y))