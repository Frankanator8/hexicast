class GameManager:
    def __init__(self, playerManager, spellManager, gameNetworking, screenMaster):
        self.playerManager = playerManager
        self.gameNetworking = gameNetworking
        self.screenMaster = screenMaster
        self.spellManager = spellManager
        self.started = False
        self.gameUpdates = gameNetworking.gameUpdates

    def startGame(self):
        if not self.started:
            self.started = True
            self.gameNetworking.connect()
            while True:
                if self.gameNetworking.gameData != {} and self.gameNetworking.gameData is not None:
                    break

            self.playerManager.makePlayers()
            self.screenMaster.screenID = 10

    def updateGameData(self):
        data = {}
        myPlayer = self.playerManager.getMyPlayer()
        data["pos"] = (myPlayer.x, myPlayer.y, myPlayer.z, myPlayer.direction)
        healthChanges = {}
        for uuid, player in self.playerManager.players.items():
            healthChanges[uuid] = player.stats.hp - self.playerManager.prevHealths[uuid]
        print(healthChanges)
        data["healthChanges"] = healthChanges
        addedSpells = {}
        for key, value in self.spellManager.unsentSpells.items():
            addedSpells[key] = value.getDictObject()

        data["newSpells"] = addedSpells
        delSpells = {}
        for key, value in self.spellManager.removeSpells.items():
            delSpells[key] = value.getDictObject()

        data["deletedSpells"] = delSpells

        if self.gameUpdates > self.gameNetworking.gameUpdates:
            self.flush()
            self.gameUpdates = self.gameNetworking.gameUpdates

        return data

    def flush(self):
        self.spellManager.unsentSpells = {}
        self.spellManager.removeSpells = {}
        for uuid, player in self.playerManager.players.items():
            self.playerManager.prevHealths[uuid] = player.stats.hp
