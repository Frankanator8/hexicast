import pygame

class MusicMaster:
    def __init__(self):
        self.loadMusic = ""
        self.currentMusic = ""
        self.transition = False
        self.volume = 1
    def playMusic(self, file):
        file = f"assets/audio/{file}"
        if file != self.currentMusic and file != self.loadMusic:
            self.loadMusic = file
            self.transition = True
            self.volume = 1

    def tick(self, dt):
        if self.transition:
            self.volume -= 0.5*dt

            if self.volume < 0:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load(self.loadMusic)
                pygame.mixer.music.play(loops=-1)
                self.currentMusic = self.loadMusic
                self.loadMusic = ""
                self.transition = False
                self.volume = 1

        pygame.mixer.music.set_volume(self.volume)