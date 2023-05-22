import requests.exceptions

from networking.network import Networking
import threading
import time

class GameNetworking(Networking):
    def __init__(self):
        super().__init__("https://spring-codefest-server.frankanator433.repl.co",
                         "wss://spring-codefest-server.frankanator433.repl.co/game")
        self.uuid = ""
        self.gameUuid = ""
        self.prospectiveGameUuid = ""
        self.games = {}
        self.uuidToName = {}
        self.gameStatus = ""
        self.gameData = {}

        self.nameQueue = []
        self.gameDataRequestTime = 0.01
        self.tries = 0

        self.gameUpdateTime = 0.01
        self.updateTries = 0
        self.updating = False
        self.updatingPos = False
        self.queue = []
        self.sendTimeout = 0
        self.playerPos = (0, 0, 1, "n")

    def __join(self, name):
        self.uuid = self.post("join", {"name":name})

    def join(self, name):
        threading.Thread(target=self.__join, args=(name, ), daemon=True).start()

    def __createGame(self, name, settings):
        self.gameUuid = self.post("createGame", {"name":name, "settings":settings, "uuid":self.uuid})
        self.prospectiveGameUuid = self.gameUuid
        self.__joinGame()
    def createGame(self, name, settings):
        threading.Thread(target=self.__createGame, args=(name, settings), daemon=True).start()

    def __getGames(self):
        self.games = self.get("getGames")
    def getGames(self):
        threading.Thread(target=self.__getGames).start()

    def __loopGetGames(self):
        while True:
            try:
                self.__getGames()

            except requests.exceptions.JSONDecodeError:
                pass
            time.sleep(1)

    def loopGetGames(self):
        threading.Thread(target=self.__loopGetGames, daemon=True).start()

    def __getName(self, uuid):
        if uuid not in self.uuidToName.keys() and uuid not in self.nameQueue:
            self.nameQueue.append(uuid)
            self.uuidToName[uuid] = self.get("getName", uuid=uuid)
            self.nameQueue.remove(uuid)

    def getName(self, uuid):
        threading.Thread(target=self.__getName, args=(uuid, ), daemon=True).start()

    def __joinGame(self):
        self.post("joinGame", {"uuid":self.uuid, "game_id":self.prospectiveGameUuid})
        self.gameUuid = self.prospectiveGameUuid

    def joinGame(self):
        threading.Thread(target=self.__joinGame, daemon=True).start()

    def __loopGameState(self):
        while True:
            if self.gameUuid != "":
                self.gameStatus = self.post("gameState", {"uuid":self.gameUuid})
            time.sleep(1)

    def loopGameState(self):
        threading.Thread(target=self.__loopGameState, daemon=True).start()

    def __loopUpdateGame(self):
        while True:
            if self.gameUuid != "":
                data = self.sendWS({"uuid":self.uuid, "request":"updatePos", "pos":self.playerPos})
                self.gameData = data


    def loopUpdateGame(self):
        threading.Thread(target=self.__loopUpdateGame, daemon=True).start()

    def updatePos(self, player):
        self.playerPos = (player.x, player.y, player.z, player.direction)

