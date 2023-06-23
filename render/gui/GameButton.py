import pygame

from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button


class GameButton(Button):
    def __init__(self, x, y, gameUUID, color, font, screen_width, gameNetworking, guiRenderer):
        self.gameNetworking = gameNetworking
        self.uuid = gameUUID
        game = gameNetworking.games[gameUUID]
        self.guiRenderer = guiRenderer
        super().__init__(x, y, [Renderable(pygame.Rect(x, y, screen_width-x-10, font[1]*2+2), color, 3),
                                Renderable(Text(f"{game['name']} - {len(game['players'])}/{game['settings']['maxPlayers']} ({'Rated' if game['settings']['rated'] else 'Unrated'})\nHost:loading...", font, (0, 0, 0), (x+1, y+1)))],
                         self.on_hover,self.on_unhover,lambda:None,self.on_release)

    def on_hover(self):
        self.renderables[0].rect.w+=4
        self.renderables[0].rect.h+=4
        self.recalculateWH()

    def on_unhover(self):
        self.renderables[0].rect.w-=4
        self.renderables[0].rect.h-=4
        self.recalculateWH()


    def on_release(self):
        self.guiRenderer.get_element("gameName").renderables[0].text.set_text(self.gameNetworking.games[self.uuid]["name"])
        players = self.gameNetworking.games[self.uuid]['players']
        playerText = "Players:"
        for player in players:
            self.gameNetworking.getName(player)
            while True:
                try:
                    playerText = f"{playerText}\n{self.gameNetworking.uuidToName[player]}"
                    break

                except KeyError:
                    pass

        self.guiRenderer.get_element("playerList").renderables[0].text.set_text(playerText)
        self.gameNetworking.prospectiveGameUuid = self.uuid


    def tick(self, dt, mousePos, mouseClicked, prevClicked, keys, prevKeys):
        super().tick(dt, mousePos, mouseClicked, prevClicked, keys, prevKeys)
        try:
            game = self.gameNetworking.games[self.uuid]
            try:
                hostName = self.gameNetworking.uuidToName[game['host']]

            except KeyError:
                hostName = "loading"

            self.renderables[1].text.set_text(f"{game['name']} - {len(game['players'])}/{game['settings']['maxPlayers']} ({'Rated' if game['settings']['rated'] else 'Unrated'})\nHost:{hostName}")

        except KeyError:
            pass


