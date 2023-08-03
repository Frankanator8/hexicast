import pygame

from audio.soundlibrary import SoundLibrary
from render.fonts import Fonts
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button


class MapButton(Button):
    soundMaster = None
    def __init__(self, x, y, w, h, mapName, mapData, mapViewer, mapButtons):
        super().__init__(x, y, [Renderable(pygame.Rect(x, y, w, h), (54, 255, 225), 4),
                                Renderable(Text(mapName, Fonts.font18, (0, 0, 0), (x+4, y+4)))], self.hover, lambda:None, lambda:None, self.select)
        self.mapButtons = mapButtons
        self.mapName = mapName
        self.mapInfo = mapData
        self.selected = False
        self.mapViewer = mapViewer

    def hover(self):
        self.mapViewer.setMapData(self.mapInfo)
        self.soundMaster.playSound(SoundLibrary.CLICK)


    def select(self):
        for mapButton in self.mapButtons:
            mapButton.selected = False
            mapButton.renderables[0].color = (54, 255, 255)

        self.selected = True
        self.renderables[0].color = (161, 255, 241)
        self.soundMaster.playSound(SoundLibrary.SELECT)
