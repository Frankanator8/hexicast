from game.player import Player


class PlayerManager:
    def __init__(self, gameNetworking, map, iRenderer):
        self.gameNetworking = gameNetworking
        self.map = map
        self.iRenderer = iRenderer
        self.players = {}

    def makePlayers(self):
        players = self.gameNetworking.gameData["gameData"]["playerPos"]
        for uuid, pos in players.items():
            p = Player(pos[0], pos[1], pos[2], 1)
            p.uuid = uuid
            self.players[uuid] = p
            self.gameNetworking.getName(uuid)
            p.name = "loading..."
            self.iRenderer.addEntity(p)

    def tick(self, keys, prevKeys, dt):
        self.players[self.gameNetworking.uuid].tickKeys(keys, prevKeys, dt, self.map)
        for uuid, pos in self.gameNetworking.gameData["gameData"]["playerPos"].items():
            p = self.players[uuid]
            p.stats.hp = self.gameNetworking.gameData["gameData"]["playerHealth"][uuid]
            p.trueHP = p.stats.hp
            if uuid != self.gameNetworking.uuid:
                p.x, p.y, p.z, p.direction = pos

            try:
                p.name = self.gameNetworking.uuidToName[uuid]

            except KeyError:
                p.name = "loading..."

    def getMyPlayer(self):
        return self.players[self.gameNetworking.uuid]

