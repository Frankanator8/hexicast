import math
from tools import Line

class IsometricMap:
    def __init__(self, map):
        with open(map) as f:
            self.data = [[[int(x) for x in c.split("/")] for c in x.strip().split()] for x in f.readlines()]
        self.generateZProfiles()
        self.generateShadowMap()
    def generateZProfiles(self):
        self.zProfiles = []
        self.maxHeight = 0
        for row in self.data:
            for tile in row:
                if len(tile) > self.maxHeight:
                    self.maxHeight = len(tile)

        for i in range(self.maxHeight):
            self.zProfiles.append([])
            for y in range(len(self.data)):
                self.zProfiles[-1].append([])
                for x in range(len(self.data[y])):
                    self.zProfiles[-1][-1].append(None)

        for x, row in enumerate(self.data):
            for y, tile in enumerate(row):
                for z, block in enumerate(tile):
                    self.zProfiles[z][y][x] = block

    def generateShadowMap(self):
        self.shadowMap = []
        for y in range(len(self.data)):
            self.shadowMap.append([])
            for x in range(len(self.data[y])):
                self.shadowMap[-1].append(0)

        for y, row in enumerate(self.data):
            for x, tile in enumerate(row):
                thisHeight = len(tile)-1
                for i in range(y-1, -1, -1):
                    if len(self.data[i][x]) > thisHeight:
                        break

                    self.shadowMap[i][x] = max(self.shadowMap[i][x], thisHeight)
                    thisHeight -= 1
                    if thisHeight <= 0:
                        break
