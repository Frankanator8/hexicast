from audio.soundlibrary import SoundLibrary
from game.player import Player


class PlayerManager:
    soundMaster = None
    def __init__(self, gameNetworking, map, iRenderer):
        self.gameNetworking = gameNetworking
        self.map = map
        self.iRenderer = iRenderer
        self.players = {}

        self.playerPoses = {}
        self.truePoses = {}

        self.lowHealthSoundUuid = ""

    def reset(self):
        self.players = {}
        self.playerPoses = {}
        self.truePoses = {}
        self.lowHealthSoundUuid = ""

    def makePlayers(self):
        players = self.gameNetworking.gameData["gameData"]["playerPos"]
        for uuid, pos in players.items():
            p = Player(pos[0], pos[1], pos[2], 1)
            p.uuid = uuid
            if self.gameNetworking.uuid == p.uuid:
                p.me = True
            self.players[uuid] = p
            self.playerPoses[uuid] = []
            self.truePoses[uuid] = (pos[0], pos[1], pos[2])
            self.gameNetworking.getName(uuid)
            p.name = "loading..."
            self.iRenderer.addEntity(p)

    def tick(self, keys, prevKeys, dt, ticks):
        self.players[self.gameNetworking.uuid].tickKeys(keys, prevKeys, dt, self.map)
        for uuid, pos in self.gameNetworking.gameData["gameData"]["playerPos"].items():
            p = self.players[uuid]
            lastHp = p.stats.hp
            p.stats.hp = self.gameNetworking.gameData["gameData"]["playerHealth"][uuid]
            if uuid == self.gameNetworking.uuid:
                if p.stats.hp < p.stats.maxHP * 0.25:
                    if not self.soundMaster.isPlaying(self.lowHealthSoundUuid):
                        self.lowHealthSoundUuid = self.soundMaster.playSound(SoundLibrary.LOWHEALTH)

                if lastHp > p.stats.hp:
                    self.soundMaster.playSound(SoundLibrary.DAMAGE)

            p.alive = self.gameNetworking.gameData["gameData"]["alive"][uuid]
            if not p.alive:
                p.image = "tombstone"

            else:
                p.image = "p1"

            if p.uuid != self.gameNetworking.uuid:
                targetX, targetY, targetZ, p.direction = pos
                if (targetX, targetY, targetZ) != self.truePoses[p.uuid]:
                    p.x, p.y, p.z = self.truePoses[p.uuid]
                    if ticks < 1:
                        ticks = 1

                    self.playerPoses[p.uuid] = []
                    for i in range(1, ticks+1):
                        self.playerPoses[p.uuid].append((p.x + i/ticks * (targetX-p.x), p.y + i/ticks * (targetY-p.y), p.z + i/ticks * (targetZ-p.z)))

                    self.truePoses[p.uuid] = (targetX, targetY, targetZ)

                if len(self.playerPoses[p.uuid]) > 0:
                    p.x, p.y, p.z = self.playerPoses[p.uuid][0]
                    self.playerPoses[p.uuid].pop(0)

                if self.gameNetworking.gameData["gameData"]["period"] == 0:
                    p.show = False

                else:
                    p.show = True

            try:
                p.name = self.gameNetworking.uuidToName[uuid]

            except KeyError:
                p.name = "loading..."


    def getMyPlayer(self):
        return self.players[self.gameNetworking.uuid]

