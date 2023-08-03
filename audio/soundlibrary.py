import loader


class SoundLibrary:
    @classmethod
    def loadSF(cls, name):
        return loader.load_sound(f"sfx/{name}.wav")
    @classmethod
    def init(cls):
        cls.CLICK = cls.loadSF("click")
        cls.GAME = cls.loadSF("game")
        cls.SELECT = cls.loadSF("select")

        cls.DAMAGE = cls.loadSF("damage")
        cls.GAMEOVER = cls.loadSF("gameover")
        cls.LOWHEALTH = cls.loadSF("lowhealth")
        cls.RUN = cls.loadSF("run")
        cls.WIN = cls.loadSF("win")

        cls.FIRE = cls.loadSF("fire")
        cls.GROUND = cls.loadSF("ground")
        cls.WATER = cls.loadSF("water")
