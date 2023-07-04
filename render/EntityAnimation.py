import os

import loader


class EntityAnimation:
    LOOP = 0
    BOUNCE = 1
    def __init__(self, folder, delay, type, direction):
        self.folder = folder
        self.delay = delay
        self.type = type
        self.direction = direction
        self.animationFrame = 0
        self.animationTime = 0

        self.forward = True

    def get_image(self, size):
        return loader.load_image(f"{self.folder}/{self.direction}/{self.animationFrame}", size=size)

    def nextFrame(self):
        if self.type == EntityAnimation.LOOP:
            self.animationFrame += 1
            if self.animationFrame >= len(os.listdir(f"assets/{self.folder}/{self.direction}")):
                self.animationFrame = 0

        else:
            if self.forward:
                self.animationFrame += 1
                if self.animationFrame + 1 >= len(os.listdir(f"assets/{self.folder}/{self.direction}")):
                    self.forward = False

            else:
                self.animationFrame -= 1
                if self.animationFrame == 0:
                    self.forward = True

    def tick(self, dt, direction):
        self.direction = direction
        self.animationTime += dt
        if self.animationTime > self.delay:
            self.animationTime -= self.delay
            self.nextFrame()