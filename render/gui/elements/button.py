from render.gui.base.element import GuiElement


class Button(GuiElement):
    def __init__(self, x, y, renderables, on_hover, on_unhover, on_click, on_release):
        super().__init__(x, y, renderables)
        self.on_hover = on_hover
        self.on_unhover = on_unhover
        self.on_click = on_click
        self.on_release = on_release
        self.hover = False
        self.click = False

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        if self.x <= mousePos[0] <= self.x + self.w and self.y <= mousePos[1] <= self.y + self.h:
            if not self.hover:
                self.on_hover()

            self.hover = True

            if mouseClicked[0]:
                if not self.click:
                    self.on_click()

                self.click = True

            else:
                if self.click:
                    self.on_release()

                self.click = False

        else:
            if self.hover:
                self.on_unhover()

            self.hover = False
            if not mouseClicked[0]:
                self.click = False
