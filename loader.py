import pygame
def load_image(name, size=None):
    image = pygame.image.load(f"assets/{name}.png").convert_alpha()
    if size != None:
        image = pygame.transform.scale(image, size)
    return image

def load_font(name, size):
    thisfont = pygame.font.Font(f"assets/font/{name}.ttf", size)
    return thisfont
