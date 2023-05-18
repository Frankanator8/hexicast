class IsometricMap:
    def __init__(self, map):
        with open(map) as f:
            self.data = [[[int(x) for x in c.split("/")] for c in x.strip().split()] for x in f.readlines()]

        print(self.data)
