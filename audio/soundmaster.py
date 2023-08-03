import uuid as UUID
import pygame
import loader


class SoundMaster:
    def __init__(self):
        self.sounds = {}
        self.channelPlaying = {}
        self.uuidPlaying = {}
        self.needToPlay = []
        self.volumes = {}
        self.volume = 1
        self.channels = set()

    def set_volume(self, v):
        self.volume = v

    def playSound(self, sound, volume=1):
        if isinstance(sound, str):
            sound = loader.load_sound(sound)

        uuid = str(UUID.uuid4())
        self.sounds[uuid] = (sound, volume)
        self.needToPlay.append(uuid)
        return uuid

    def tick(self):
        indexOffset = 0
        for index in range(len(self.needToPlay)):
            sound = self.needToPlay[index-indexOffset]
            channel = pygame.mixer.find_channel(force=True)
            if channel not in self.channels:
                self.channels.add(channel)

            channel.play(self.sounds[sound][0])
            self.channelPlaying[channel] = sound
            self.uuidPlaying[sound] = channel
            self.volumes[sound] = self.sounds[sound][1]
            self.needToPlay.pop(index-indexOffset)
            indexOffset += 1

        for channel in self.channels:
            channel.set_volume(self.volume * self.volumes[self.channelPlaying[channel]])

    def isPlaying(self, uuid):
        try:
            channel = self.uuidPlaying[uuid]

        except KeyError:
            return False

        if channel.get_busy():
            if self.channelPlaying[channel] == uuid:
                return True

            else:
                return False

        else:
            return False

    def loadInto(self, *args):
        for arg in args:
            arg.soundMaster = self
