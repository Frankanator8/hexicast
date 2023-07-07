from game.entity import Entity


class Decor(Entity):
    def __init__(self, x, y, z, image, direction, animation=None):
        super().__init__(x, y, z, image, direction, animation=animation)

    def tick(self, player, dt):
        pass