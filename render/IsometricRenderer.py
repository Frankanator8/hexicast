import math

import loader


class IsometricRenderer:
    TILE_SIZE = (96, 96)
    @classmethod
    def init(cls):
        cls.GRASS = loader.load_image("map/grass", size=cls.TILE_SIZE)
        cls.STONE = loader.load_image("map/water", size=cls.TILE_SIZE)
    def __init__(self, screen, camera):
        self.screen = screen
        self.camera = camera
        self.entities = []

    def addEntity(self, entity):
        self.entities.append(entity)

    def render(self, map):
        display = self.screen
        camera = self.camera
        size = self.TILE_SIZE
        placeDicts = {}
        for entity in self.entities:
            if (math.floor(entity.x), math.floor(entity.y)) not in placeDicts.keys():
                placeDicts[(math.floor(entity.x), math.floor(entity.y))] = []
            placeDicts[(math.floor(entity.x), math.floor(entity.y))].append(entity)

        # TODO: Shadows and https://stackoverflow.com/questions/892811/drawing-isometric-game-worlds
        for y, row in enumerate(map.data):
            for x, cell in enumerate(row):
                for z, block in enumerate(cell):
                    if block:
                        tex = self.GRASS

                    else:
                        tex = self.STONE
                    oldY = y
                    oldX = x
                    x -= camera.x
                    y -= camera.y

                    cart_x = x * size[0]/2
                    cart_y = y * size[1]/2
                    iso_x = cart_x - cart_y
                    iso_y = (cart_x + cart_y) / 2.153 - z * size[1]

                    iso_x += display.get_width()/2
                    iso_y += display.get_height()/2
                    if not (iso_x+size[0] < 0 or iso_x > display.get_width() or iso_y+size[1] < 0 or iso_y > display.get_height()):
                        display.blit(tex, (iso_x, iso_y))
                    y = oldY
                    x = oldX

                    if (x, y) in placeDicts.keys():
                        for entity in placeDicts[(x, y)]:
                            cameraX = entity.x - camera.x
                            cameraY = entity.y - camera.y
                            cart_x = cameraX * size[0]/2
                            cart_y = cameraY * size[1]/2
                            iso_x = cart_x - cart_y
                            iso_y = (cart_x + cart_y) / 2.153 - size[1] * (entity.z - 1)
                            display.blit(loader.load_image(f"{entity.image}/{entity.direction}", size=size), (iso_x+display.get_width()/2, iso_y+display.get_height()/2))