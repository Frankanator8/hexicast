class GuiRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.elements = []
        self.tags = {}
        self.back = []

    def add_element(self, element, tag=None, back=False):
        self.elements.append(element)
        if tag is not None:
            self.tags[tag] = element

        if back:
            self.back.append(element)

    def get_element(self, tag):
        if tag not in self.tags.keys():
            return None

        return self.tags[tag]

    def has_element(self, tag):
        return tag in self.tags.keys()

    def render(self, screen):
        for element in self.back:
            if element.show:
                element.render(screen)

        for element in self.elements:
            if element not in self.back:
                if element.show:
                    element.render(screen)

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        for element in self.elements:
            if element.show:
                element.tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)

    def remove_element(self, tag):
        self.elements.remove(self.tags[tag])
        if self.tags[tag] in self.back:
            self.back.remove(self.tags[tag])
        del self.tags[tag]

