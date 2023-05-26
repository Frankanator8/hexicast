class GameManager:
    def __init__(self, playerManager, spellManager, gameNetworking, screenMaster):
        self.playerManager = playerManager
        self.gameNetworking = gameNetworking
        self.screenMaster = screenMaster
        self.spellManager = spellManager
        self.started = False

    def startGame(self):
        if not self.started:
            self.started = True
            while True:
                if self.gameNetworking.gameData != {} and self.gameNetworking is not None:
                    break

            self.playerManager.makePlayers()
            self.screenMaster.screenID = 10