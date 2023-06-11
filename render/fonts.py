import loader


class Fonts:
    font24 = None
    font24 = None
    font48 = None
    font24 = None
    font150 = None
    font150 = None
    font48 = None
    font150 = None
    font24 = None
    font48 = None
    font24 = None
    font18 = None

    @classmethod
    def init(cls):
        cls.font24 = (loader.load_font("theFont", 24), 24)
        cls.font48 = (loader.load_font("theFont", 48), 48)
        cls.font18 = (loader.load_font("theFont", 18), 18)
        cls.font150 = (loader.load_font("theFont", 150), 150)
