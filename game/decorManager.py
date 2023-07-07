from random import Random

from game.decor import Decor
from game.decors.WaterShine import WaterShine
from render.EntityAnimation import EntityAnimation


class DecorManager:
    def __init__(self, gameNetworking, renderer):
        self.gameNetworking = gameNetworking
        self.isometricRenderer = renderer
        self.random = Random()
        self.decors = []
        self.addedGrasses = set()

    def reset(self):
        self.decors = []
        self.addedGrasses = set()

    def makeGrassPatch(self, x, y, depth, amt):
        if depth == 0:
            return
        for oY in range(-amt, amt+1):
            for oX in range(-amt, amt+1):
                if (x+oX, y+oY) not in self.addedGrasses:
                    if x+oX >= 0 and y+oY >= 0:
                        try:
                            if self.isometricRenderer.map.data[y+oY][x+oX][-1] == 1:
                                self.add_decor(Decor(x+oX, y+oY, len(self.isometricRenderer.map.data[y+oY][x+oX])-2,
                                                     "map/grassEntity", "n",
                                                     animation=EntityAnimation("map/grassEntity", 0.25, EntityAnimation.BOUNCE, "n")))
                                self.addedGrasses.add((x+oX, y+oY))

                        except IndexError:
                            pass

        self.makeGrassPatch(x+self.random.choice([-1, 1]), y+self.random.choice([-1, 1]), depth-1, amt)


    def init(self):
        seed = 0
        for letter in self.gameNetworking.gameUuid:
            seed += ord(letter)
        self.random = Random()
        self.random.seed(seed)

        grasses = []
        waters = []
        for y, row in enumerate(self.isometricRenderer.map.data):
            for x, cell in enumerate(row):
                if cell[-1] == 1:
                    grasses.append((x, y))

                elif cell[-1] == 0:
                    waters.append((x, y))


        for i in range(self.random.randint(5, 7)):
            self.makeGrassPatch(*self.random.choice(grasses), self.random.randint(2, 7), self.random.randint(2, 3))

        for i in range(35):
            x, y = self.random.choice(waters)
            self.add_decor(WaterShine(x, y, len(self.isometricRenderer.map.data[y][x])-2, waters, self.isometricRenderer.map))

    def add_decor(self, decor):
        self.decors.append(decor)
        self.isometricRenderer.addEntity(decor)

    def tick(self, player, dt):
        for decor in self.decors:
            decor.tick(player, dt)