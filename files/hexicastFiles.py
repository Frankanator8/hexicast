from files.appFiles import AppSupport


class HexicastFiles(AppSupport):
    def __init__(self, musicMaster, soundMaster):
        super().__init__("hexicast")
        self.musicMaster = musicMaster
        self.soundMaster = soundMaster
        self.uuid = ""
        self.lastSavedSettings = ""

    def loadSettings(self):
        if not self.file_exists("settings.txt"):
            self.writeSettings()
        settingsData = self.read_data("settings.txt")
        music, sfx = tuple([float(i.split("=")[1]) for i in settingsData.split()])
        self.musicMaster.set_volume(music)
        self.soundMaster.set_volume(sfx)
        self.lastSavedSettings = settingsData

    def writeSettings(self):
        toWrite = f"music={self.musicMaster.volume}\nsound={self.soundMaster.volume}"
        if toWrite != self.lastSavedSettings:
            try:
                self.write_data("settings.txt", toWrite)
                self.lastSavedSettings = toWrite

            except OSError:
                pass

    def retrieveUuid(self):
        if not self.file_exists("uuid.txt"):
            self.uuid = ""
            return

        self.uuid = self.read_data("uuid.txt")

    def writeUuid(self, uuid):
        if uuid != self.uuid and uuid != "":
            self.write_data("uuid.txt", uuid)
            self.uuid = uuid