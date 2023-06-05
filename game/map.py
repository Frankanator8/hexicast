from tools import Line
import math

class Map:
    def __init__(self, iMap):
        self.data = iMap.data

    def considerOutOfWorld(self, x, y):
        if y < 0:
            y = 0
        if y >= len(self.data):
            y = len(self.data)-0.01

        if x < 0:
            x = 0
        if x >= len(self.data[math.floor(y)]):
            x = len(self.data[math.floor(y)])-0.01

        return (x, y)

    def findCollisionPoint(self, x, y, entity):
        if y < 0:
            y = 0
        if y >= len(self.data):
            y = len(self.data)-0.01

        if x < 0:
            x = 0
        if x >= len(self.data[math.floor(y)]):
            x = len(self.data[math.floor(y)])-0.01
        if len(self.data[math.floor(y)][math.floor(x)]) > math.floor(entity.z):
            line1 = Line.determineFromPoints(x, y, entity.x, entity.y)
            uLine = Line(0, math.floor(y)-0.01)
            bLine = Line(0, math.floor(y)+1.01)
            lLine = Line(10000000, math.floor(x)-0.01)
            rLine = Line(10000000, math.floor(x)+1.01)
            uInt = uLine.intersect(line1)
            bInt = bLine.intersect(line1)
            lInt = lLine.intersect(line1)
            rInt = rLine.intersect(line1)

            ret = (entity.x, entity.y)
            if (math.floor(x) <= uInt[0] <= math.floor(x)+1) and (min(y, entity.y) <= uInt[1] <= max(y, entity.y)):
                ret = uInt

            if (math.floor(x) <= bInt[0] <= math.floor(x)+1) and (min(y, entity.y) <= bInt[1] <= max(y, entity.y)):
                ret = bInt

            if (math.floor(y) <= lInt[1] <= math.floor(y)+1) and (min(x, entity.x) <= lInt[0] <= max(x, entity.x)):
                ret = lInt

            if (math.floor(y) <= rInt[1] <= math.floor(y)+1) and (min(x, entity.x) <= rInt[0] <= max(x, entity.x)):
                ret = rInt

            return ret

        else:
            return (x, y)