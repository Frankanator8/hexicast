import random
from mapGenerator import MapMaker
with open("/Users/Frank/IntelliJProjects/springcodefest2023/assets/map.txt", "w") as f:
    maker = MapMaker(50, 50)
    maker.generate()
    for i in range(maker.h):
        line = ""
        for j in range(maker.w):
            this = ""
            for index, k in enumerate(maker.map[i][j]):
                if index!= len(maker.map[i][j]) - 1:
                    this += str(k) + "/"

                else:
                    this += str(k)

            line += this + " "
        f.write(line + "\n")
