import requests.exceptions

from networking.network import Networking
import threading
import time

class GameNetworking(Networking):
    def __init__(self):
        super().__init__("https://hexicast-server.frankanator433.repl.co",
                         "wss://hexicast-server.frankanator433.repl.co/game")
        # super().__init__("http://localhost:7070",
        #                  "ws://localhost:7070/game")
        self.uuid = ""
        self.gameUuid = ""
        self.prospectiveGameUuid = ""
        self.games = {}
        self.uuidToName = {}
        self.gameStatus = ""
        self.gameData = {}
        self.userData = {}
        self.userDataQueue = set()
        self.mapInfo = []

        self.nameQueue = []
        self.gameDataRequestTime = 0.01
        self.tries = 0

        self.sendGameData = {}
        self.lastSentUuid = ""
        self.sendUuid = ""

        self.accountUuid = ""

        self.signinMessage = ""
        self.joinPrivateGameMessage = ""
        self.createPrivateGameMessage = ""

    def reset(self):
        self.gameStatus = ""
        self.gameData = {}
        self.gameUuid = ""
        self.prospectiveGameUuid = ""
        self.sendGameData = {}
        self.lastSentUuid = ""
        self.sendUuid = ""

    def __getMapInfo(self):
        self.mapInfo = self.get("maps")

    def getMapInfo(self):
        threading.Thread(target=self.__getMapInfo, daemon=True).start()

    def __login(self, username, pw):
        res = super().post("login", {"name":username, "pw":pw})
        if res.split()[0] == "SUCCESS":
            self.accountUuid = res.split()[1]
            self.__join(" ".join(res.split()[2:]))

        elif res.split()[0] == "NOACCEX":
            self.signinMessage = "No account exists"

        elif res.split()[0] == "INCUSERPW":
            self.signinMessage = "Wrong password"

    def login(self, username, pw):
        threading.Thread(target=self.__login, args=(username, pw, ), daemon=True).start()

    def __signup(self, name, display, pw):
        res = super().post("signup", {"name":name, "display":display, "pw":pw})
        if res == "GOOD":
            self.__login(name, pw)

        else:
            self.signinMessage = "Unavailable"

    def signup(self, name, display, pw):
        threading.Thread(target=self.__signup, args=(name, display, pw, ), daemon=True).start()

    def __getUserInfo(self, username, uuid):
        self.userDataQueue.add(username)
        if uuid:
            res = self.get("getInfoByUuid", uuid=username)

        else:
            res = self.get("getInfo", username=username)

        if res != "DNE":

            self.userData[username] = res
            self.userDataQueue.remove(username)

    def getUserInfo(self, username, uuid=False):
        if username not in self.userDataQueue and username not in self.userData.keys():
            threading.Thread(target=self.__getUserInfo, args=(username, uuid, ), daemon=True).start()


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

    def __createPrivateGame(self, name, settings):
        res = self.post("createPrivateGame", {"name":name, "settings":settings, "uuid":self.uuid})
        if res != "No":
            self.gameUuid = res
            self.prospectiveGameUuid = self.gameUuid
            self.__joinGame()

        else:
            self.createPrivateGameMessage = "Code already in use"

    def createPrivateGame(self, name, settings):
        threading.Thread(target=self.__createPrivateGame, args=(name, settings, ), daemon=True).start()


    def __joinPrivateGame(self, code):
        ret = self.post("joinPrivateGame", {"uuid":self.uuid, "game_id":code})
        if ret == "Full game" or ret == "Game does not exist":
            self.joinPrivateGameMessage = ret

        else:
            self.gameUuid = ret
            self.prospectiveGameUuid = ret

    def joinPrivateGame(self, code):
        threading.Thread(target=self.__joinPrivateGame, args=(code, ), daemon=True).start()

    def __getGames(self):
        self.games = self.get("getGames")
    def getGames(self):
        threading.Thread(target=self.__getGames).start()

    def __loopGetGames(self):
        while True:
            if self.closed:
                return
            try:
                self.__getGames()

            except (requests.exceptions.JSONDecodeError, requests.exceptions.ConnectionError):
                pass

            time.sleep(1)

    def loopGetGames(self):
        threading.Thread(target=self.__loopGetGames, daemon=True).start()

    def __getName(self, uuid):
        self.nameQueue.append(uuid)
        self.uuidToName[uuid] = self.get("getName", uuid=uuid)
        self.nameQueue.remove(uuid)

    def getName(self, uuid):
        if uuid not in self.uuidToName.keys() and uuid not in self.nameQueue:
            threading.Thread(target=self.__getName, args=(uuid, ), daemon=True).start()

    def __joinGame(self):
        self.post("joinGame", {"uuid":self.uuid, "game_id":self.prospectiveGameUuid})
        self.gameUuid = self.prospectiveGameUuid

    def joinGame(self):
        threading.Thread(target=self.__joinGame, daemon=True).start()

    def __loopGameState(self):
        while True:
            if self.closed:
                return

            if self.gameUuid != "":
                self.gameStatus = self.post("gameState", {"uuid":self.gameUuid})
            time.sleep(1)

    def loopGameState(self):
        threading.Thread(target=self.__loopGameState, daemon=True).start()

    def __loopUpdateGame(self):
        while True:
            if self.closed:
                return
            if self.gameUuid != "":
                if self.sendGameData != {}:
                    sendData = {"uuid":self.uuid, "request":"update"}
                    sendData.update(self.sendGameData)
                    data = self.sendWS(sendData)
                    self.gameData = data

                else:
                    sendData = {"uuid":self.uuid, "request":"get"}
                    data = self.sendWS(sendData)
                    self.gameData = data

                self.lastSentUuid = self.sendUuid

            else:
                self.sendWS({"uuid":self.uuid, "request":"ping"})


    def loopUpdateGame(self):
        threading.Thread(target=self.__loopUpdateGame, daemon=True).start()

    def __queue(self):
        self.prospectiveGameUuid = self.post("queue", {"accountUuid": self.accountUuid, "uuid":self.uuid})
        self.__joinGame()

    def queue(self):
        threading.Thread(target=self.__queue, daemon=True).start()
