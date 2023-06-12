import loader


class Fonts:
    @classmethod
    def init(cls):
        cls.font15 = (loader.load_font("theFont", 15), 15)
        cls.font24 = (loader.load_font("theFont", 24), 24)
        cls.font36 = (loader.load_font("theFont", 36), 36)
        cls.font48 = (loader.load_font("theFont", 48), 48)
        cls.font18 = (loader.load_font("theFont", 18), 18)
        cls.font150 = (loader.load_font("theFont", 150), 150)
