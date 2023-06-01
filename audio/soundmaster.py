import uuid as UUID
import pygame
import loader


class SoundMaster:
    def __init__(self):
        self.sounds = {}
        self.needToPlay = []
        self.volume = 1
        self.channels = set()

    def set_volume(self, v):
        self.volume = v

    def playSound(self, sound):
        if isinstance(sound, str):
            sound = loader.load_sound(sound)

        uuid = UUID.uuid4()
        self.sounds[uuid] = sound
        self.needToPlay.append(uuid)
        return uuid

    def tick(self):
        for sound in self.needToPlay:
            channel = pygame.mixer.find_channel(force=True)
            if channel not in self.channels:
                self.channels.add(channel)

            channel.play(self.sounds[sound])

        for channel in self.channels:
            channel.set_volume(self.volume)
