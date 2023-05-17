class IsometricMap:
    def __init__(self, map):
        with open(map) as f:
            self.data = [[int(c) for c in x.strip()] for x in f.readlines()]
