import tools


class GameSound:
    def __init__(self, soundMaster, playerManager, spellManager, gameNetworking):
        self.soundMaster = soundMaster
        self.playerManager = playerManager
        self.spellManager = spellManager
        self.gameNetworking = gameNetworking
    def getDistSoundFactor(self, dist):
        if dist <= 0:
            dist = 0.01

        if dist > 10:
            return 0

        soundFactor = 1/dist
        if soundFactor > 1:
            soundFactor = 1

        return soundFactor
    def getPointSoundFactor(self, listener, source):
        return self.getDistSoundFactor(tools.dist(*listener, *source))
    def getSoundFactor(self, pos):
        return self.getPointSoundFactor(self.playerManager.getMyPlayer().x, self.playerManager.getMyPlayer().y, *pos)

    def reset(self):
        pass



