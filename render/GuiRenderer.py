class GuiRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.elements = []
        self.tags = {}

    def add_element(self, element, tag=None):
        self.elements.append(element)
        if tag is not None:
            self.tags[tag] = element

    def get_element(self, tag):
        if tag not in self.tags.keys():
            return None

        return self.tags[tag]

    def render(self, screen):
        for element in self.elements:
            if element.show:
                element.render(screen)

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        for element in self.elements:
            if element.show:
                element.tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)

    def remove_element(self, tag):
        self.elements.remove(self.tags[tag])
        del self.tags[tag]

