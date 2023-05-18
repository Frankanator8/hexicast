import random
with open("/Users/Frank/IntelliJProjects/springcodefest2023/assets/map.txt", "w") as f:
    for i in range(100):
        line = ""
        for j in range(100):
            this = ""
            seed = random.randint(1, 20)

            if seed == 20:
                height = 3
            if 12 <= seed < 20:
                height = 2

            else:
                height = 1
            for k in range(height):
                if k!=height-1:
                    this += str(random.randint(0, 1)) + "/"

                else:
                    this += str(random.randint(0, 1))

            line += this + " "
        print(line)
        f.write(line + "\n")
