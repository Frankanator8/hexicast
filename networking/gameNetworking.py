from networking.network import Networking
import threading

class GameNetworking(Networking):
    def __init__(self):
        super().__init__("https://spring-codefest-server.frankanator433.repl.co")
        self.uuid = ""
        self.gameUuid = ""
        self.games = {}

    def __join(self, name):
        self.uuid = self.post("join", {"name":name})
    def join(self, name):
        threading.Thread(target=self.__join, args=(name, ), daemon=True).start()

    def __createGame(self, name, settings):
        self.gameUuid = self.post("createGame", {"name":name, "settings":settings, "uuid":self.uuid})
    def createGame(self, name, settings):
        threading.Thread(target=self.__createGame, args=(name, settings), daemon=True).start()

    def __getGames(self):
        self.games = self.get("getGames")
    def getGames(self):
        threading.Thread(target=self.__getGames).start()

    def __loopGetGames(self):
        while True:
            self.__getGames()

    def loopGetGames(self):
        threading.Thread(target=self.__loopGetGames, daemon=True).start()

