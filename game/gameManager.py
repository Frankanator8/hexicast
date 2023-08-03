class GameManager:
    def __init__(self, playerManager, spellManager, gameNetworking, screenMaster, timeManager, decorManager, gameSound):
        self.playerManager = playerManager
        self.gameNetworking = gameNetworking
        self.screenMaster = screenMaster
        self.spellManager = spellManager
        self.timeManager = timeManager
        self.decorManager = decorManager
        self.gameSound = gameSound
        self.started = False
        self.ticksSinceLastUpdate = 0
        self.ticks = 0

    def startGame(self):
        if not self.started:
            self.started = True
            self.gameNetworking.connect()
            while True:
                if self.gameNetworking.gameData != {} and self.gameNetworking.gameData is not None:
                    break

            self.playerManager.makePlayers()
            self.spellManager.isometricRenderer.map.load(self.gameNetworking.gameData["gameData"]["map"])
            self.playerManager.map.data = self.spellManager.isometricRenderer.map.data
            self.decorManager.init()
            self.flush()
            self.screenMaster.screenID = 10

    def reset(self):
        self.started = False
        self.playerManager.reset()
        self.timeManager.reset()
        self.spellManager.reset()
        self.gameNetworking.reset()
        self.spellManager.isometricRenderer.reset()
        self.decorManager.reset()
        self.gameSound.reset()

    def updateGameData(self):
        data = {}
        myPlayer = self.playerManager.getMyPlayer()
        data["pos"] = (myPlayer.x, myPlayer.y, myPlayer.z, myPlayer.direction)
        healthChanges = {}
        for uuid, player in self.playerManager.players.items():
            healthChanges[uuid] = player.hpChange
        data["healthChanges"] = healthChanges
        addedSpells = {}
        for key, value in self.spellManager.unsentSpells.items():
            addedSpells[key] = value.getDictObject()

        data["newSpells"] = addedSpells
        delSpells = {}
        for key, value in self.spellManager.removeSpells.items():
            delSpells[key] = value.getDictObject()

        data["deletedSpells"] = delSpells


        return data

    def flush(self):
        self.spellManager.unsentSpells = {}
        self.spellManager.removeSpells = {}
        for player in self.playerManager.players.values():
            player.hpChange = 0
            player.trueHP = player.stats.hp

        self.ticksSinceLastUpdate = self.ticks
        self.ticks = 0
