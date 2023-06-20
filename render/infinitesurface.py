import pygame


class InfiniteSurface:
    def __init__(self, chunk_size=1000):
        self.map = {}
        self.chunk_size = chunk_size

    def __getChunk(self, x, y):
        return x//self.chunk_size, y//self.chunk_size, x%self.chunk_size, y%self.chunk_size

    def __blitOnSurface(self, image, chunkX, chunkY, x, y):
        if (chunkX, chunkY) not in self.map.keys():
            self.map[(chunkX, chunkY)] = pygame.Surface((self.chunk_size, self.chunk_size), pygame.SRCALPHA)
        self.map[(chunkX, chunkY)].blit(image, (x, y))

    def blit(self, image, x, y):
        w = image.get_width()
        h = image.get_height()

        self.__blitOnSurface(image, *self.__getChunk(x, y))
        otherChunk = self.__getChunk(x, y+h)
        self.__blitOnSurface(image, otherChunk[0], otherChunk[1], otherChunk[2], otherChunk[3]-h)
        otherChunk = self.__getChunk(x+w, y+h)
        self.__blitOnSurface(image, otherChunk[0], otherChunk[1], otherChunk[2]-w, otherChunk[3]-h)
        otherChunk = self.__getChunk(x+w, y)
        self.__blitOnSurface(image, otherChunk[0], otherChunk[1], otherChunk[2]-w, otherChunk[3])

    def render(self, screen, x, y):
        baseChunk = self.__getChunk(-x, -y)
        # not done


