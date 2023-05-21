class GuiElement:
    def __init__(self, x, y, renderables):
        self.x = x
        self.y = y
        self.renderables = renderables
        self.show = True
        self.w = 0
        self.h = 0
        self.recalculateWH()

    def recalculateWH(self):
        maxX = -100000
        minX = 100000
        maxY = -100000
        minY = 100000
        for renderable in self.renderables:
            if renderable.x < minX:
                minX = renderable.x

            if renderable.x + renderable.w > maxX:
                maxX = renderable.x + renderable.w

            if renderable.y < minY:
                minY = renderable.y

            if renderable.y + renderable.h > maxY:
                maxY = renderable.y + renderable.h

        self.w = maxX - minX
        self.h = maxY - minY

    def render(self, screen):
        for object in self.renderables:
            object.render(screen)

    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        pass

    def moveTo(self, x, y):
        diffX = x - self.x
        diffY = y - self.y
        for renderable in self.renderables:
            renderable.moveTo(renderable.x + diffX, renderable.y + diffY)

        self.x += diffX
        self.y += diffY