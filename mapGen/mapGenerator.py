import random
class MapMaker:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.map = []
        for i in range(h):
            self.map.append([])
            for j in range(w):
                self.map[-1].append([0])

    def generateMountain(self, centerx, centery):
        for y in range(-random.randint(2, 5), random.randint(2, 5)):
            for x in range(-random.randint(2, 5), random.randint(2, 5)):
                height = random.randint(5-abs(x)-abs(y), 12-abs(x)-abs(y))
                if height < 0:
                    height = 0

                for i in range(height):
                    try:
                        self.map[centery+y][centerx+x].append(2)

                    except IndexError:
                        pass

    def generateLand(self):
        startX = random.randint(0, self.w-1)
        startY = random.randint(0, self.h-1)
        while random.randint(1, 20) != 16:
            radius = random.randint(5, 10)
            hill = random.randint(1, 10) == 8
            for i in range(-radius, radius+1):
                for j in range(-radius, radius+1):
                    try:
                        self.map[startY + i][startX+j][0] = 1
                        if hill:
                            self.map[startY + i][startX+j].append(1)

                    except IndexError:
                        pass

            startX += random.randint(1, 3)
            startY += random.randint(1, 3)

    def generate(self):
        for i in range(2):
            self.generateLand()

        for i in range(random.randint(2, 4)):
            self.generateMountain(random.randint(0, self.w-1), random.randint(0, self.h-1))
