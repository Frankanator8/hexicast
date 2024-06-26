import pygame

SOUNDS = {}
IMAGES = {}

def load_image(name, size=None):
    if (name, size) in IMAGES.keys():
        return IMAGES[(name, size)].copy()
    image = pygame.image.load(f"assets/{name}.png").convert_alpha()
    if size is not None:
        image = pygame.transform.scale(image, size)
    IMAGES[(name, size)] = image
    return image

def load_font(name, size):
    thisfont = pygame.font.Font(f"assets/font/{name}.ttf", size)
    return thisfont

def load_sound(name):
    if name in SOUNDS.keys():
        return SOUNDS[name]
    sound = pygame.mixer.Sound(f"assets/audio/{name}")
    SOUNDS[name] = sound
    return sound
