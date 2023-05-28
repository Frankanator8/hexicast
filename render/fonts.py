import loader


class Fonts:
    @classmethod
    def init(cls):
        cls.font24 = (loader.load_font("theFont", 24), 24)
        cls.font48 = (loader.load_font("theFont", 48), 48)
        cls.font18 = (loader.load_font("theFont", 18), 18)
