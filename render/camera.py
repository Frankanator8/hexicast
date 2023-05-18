class Camera:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def follow(self, entity):
        self.x = entity.x
        self.y = entity.y