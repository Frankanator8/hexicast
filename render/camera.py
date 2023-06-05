import pygame


class Camera:
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen

    def follow(self, entity):
        self.x = entity.x
        self.y = entity.y

    def tickKeys(self, dt, keys, map):
        futPosition = [self.x, self.y]
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            futPosition[1] -= 10 * dt

        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            futPosition[1] += 10 * dt

        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            futPosition[0] -= 10 * dt

        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            futPosition[0] += 10 * dt



        self.x, self.y = map.considerOutOfWorld(*futPosition)