import math
import random
import threading
import uuid as UUID
import pygame
import loader
from render import fonts
from render.gui.Flair import Flair
from render.gui.GameButton import GameButton
from render.gui.SubmitButton import SubmitButton
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button
from render.gui.elements.slider import Slider
from render.gui.elements.textinput import TextInput

class GuiMaker:
    def __init__(self, screen, renderer, gameNetworking, screenMaster, gameInitializer, musicMaster, soundMaster):
        self.screen = screen
        self.gameNetworking = gameNetworking
        self.font = fonts.Fonts.font48
        self.fontS = fonts.Fonts.font24
        self.renderer = renderer
        self.w = screen.get_width()*0.381966011
        self.screenMaster = screenMaster
        self.gameInitalizer = gameInitializer
        self.musicMaster = musicMaster
        self.soundMaster = soundMaster

        self.gamePage = 0
        self.perPage = 7
        self.uuids = []
        self.uuidToButton = {}
        self.gameEndUuids = []

        self.flairs = []

    def makeInitialGui(self):
        guiRenderer = self.renderer

        blueBanner = GuiElement(0, 0, [Renderable(loader.load_image("sidebanner", size=(self.w, self.screen.get_height())), (0, 0))])
        guiRenderer.add_element(blueBanner, tag="blueBanner")
        aestheticBanner = GuiElement(self.w, 0, [Renderable(loader.load_image("tempback", size=(800, self.screen.get_height())), (self.w, 0))])
        guiRenderer.add_element(aestheticBanner, tag="aestheticBanner")
        gameLogo = GuiElement(0, 10, [Renderable(loader.load_image("logo", size=(self.w,80)), (0, 10))])
        guiRenderer.add_element(gameLogo, tag="gameLogo")
        nameInputBanner = GuiElement(10, 100, [Renderable(Text("Name:", self.font, (0, 0, 0), (10, 100)))])
        guiRenderer.add_element(nameInputBanner, tag="nameInputBanner")
        nameInput = TextInput(10, 150, Text("", self.font, (0, 0, 0), (10, 150)), maxLen=9)
        guiRenderer.add_element(nameInput, tag="nameInput")
        submitName = SubmitButton(10, 250, 200, 50, self.font, lambda:self.gameNetworking.join(nameInput.text) if nameInput.text != "" else None)
        guiRenderer.add_element(submitName, tag="submitName")

        musicBanner = GuiElement(10, self.screen.get_height()-130, [Renderable(Text("Music Volume", self.fontS, (0, 0, 0), (10, self.screen.get_height()-130)))])
        guiRenderer.add_element(musicBanner, tag="musicBanner")
        musicSlider = Slider(10, self.screen.get_height()-100, self.w-20, 20, 100, lambda x:self.musicMaster.set_volume(x/100))
        guiRenderer.add_element(musicSlider, tag="musicSlider")
        sfxBanner = GuiElement(10, self.screen.get_height()-70, [Renderable(Text("Sound FX Volume", self.fontS, (0, 0, 0), (10, self.screen.get_height()-70)))])
        guiRenderer.add_element(sfxBanner, tag="sfxBanner")
        sfxSlider = Slider(10, self.screen.get_height()-40, self.w-20, 20, 100, lambda x:self.soundMaster.set_volume(x/100))
        guiRenderer.add_element(sfxSlider, tag="sfxSlider")

    def decrementPage(self):
        if self.gamePage > 0:
            self.gamePage -= 1

    def incrementPage(self):
        if self.gamePage < math.ceil(len(self.uuids)/self.perPage) - 1:
            self.gamePage += 1

    def on_login_window(self):
        guiRenderer = self.renderer
        guiRenderer.remove_element("nameInputBanner")
        guiRenderer.remove_element("aestheticBanner")
        guiRenderer.remove_element("nameInput")
        guiRenderer.remove_element("submitName")

        lightBlueBanner = GuiElement(0, 0, [Renderable(loader.load_image("lobbyBanner", size=(self.screen.get_width()-self.w, self.screen.get_height())), (self.w, 0))])
        guiRenderer.add_element(lightBlueBanner, tag="lightBlueBanner")
        createBanner = GuiElement(self.w+10, 10, [Renderable(Text("Create a Game", self.font, (255, 170, 0), (self.w+10, 10)))])
        guiRenderer.add_element(createBanner, tag="createBanner")
        nameBanner = GuiElement(self.w+10, 60, [Renderable(Text("Name:", self.fontS, (0, 0, 0), (self.w+10, 60)))])
        guiRenderer.add_element(nameBanner, tag="nameBanner")
        gameNameInput = TextInput(self.w+70, 60, Text("", self.fontS, (0, 0, 0), (self.w+70, 60)), maxLen=18)
        guiRenderer.add_element(gameNameInput, tag="gameNameInput")
        playerCountBanner = GuiElement(self.w+350, 60, [Renderable(Text("Players:", self.fontS, (0, 0, 0), (self.w+350, 60)))])
        guiRenderer.add_element(playerCountBanner, tag="playerCountBanner")
        playerCountInput = TextInput(self.w+430, 60, Text("", self.fontS, (0, 0, 0), (self.w+430, 60)), maxLen=1)
        guiRenderer.add_element(playerCountInput, tag="playerCountInput")
        sepLine = GuiElement(self.w+3, 125, [Renderable(pygame.Rect(self.w+3, 125, self.screen.get_width() - self.w - 6, 4), (0, 0, 0), 0)])
        guiRenderer.add_element(sepLine, tag="lobbySepLine")
        gameSubmit = SubmitButton(self.w+10, 100, 100, 50, self.fontS, lambda: self.gameNetworking.createGame(gameNameInput.text,
                                                                                                              {"maxPlayers": int(playerCountInput.text)}))
        guiRenderer.add_element(gameSubmit, tag="gameSubmit")

        gameName = GuiElement(10, 100, [Renderable(Text("Choose a game", self.font, (5, 0, 149), (10, 100)))])
        guiRenderer.add_element(gameName, tag="gameName")
        passwordText = GuiElement(10, 160, [Renderable(Text("Password (if applicable)", self.fontS, (5, 0, 149), (10, 160)))])
        guiRenderer.add_element(passwordText, tag="passwordText")
        passwordInput = TextInput(10, 190, Text("", self.fontS, (0, 0, 0), (10, 190)))
        guiRenderer.add_element(passwordInput, tag="passwordInput")
        playerList = GuiElement(10, 220, [Renderable(Text("Players:", self.fontS, (5, 0, 149), (10, 220)))])
        guiRenderer.add_element(playerList, tag="playerList")
        join = SubmitButton(10, 300, 200, 75, self.font, self.gameNetworking.joinGame, text="Join!")
        guiRenderer.add_element(join, tag="joinButton")

        pageForward = Button(self.w+10, 150, [Renderable(loader.load_image("arrowB"), (self.w+10, 150))], lambda:None, lambda:None, lambda:None, self.decrementPage)
        guiRenderer.add_element(pageForward, tag="pageBackward")
        pageText = GuiElement(self.w+40, 150, [Renderable(Text("Page", self.fontS, (255, 255, 255), (self.w+40, 150)))])
        guiRenderer.add_element(pageText, tag="pageText")
        pageForward = Button(self.w+150, 150, [Renderable(loader.load_image("arrowF"), (self.w+150, 150))], lambda:None, lambda:None, lambda:None, self.incrementPage)
        guiRenderer.add_element(pageForward, tag="pageForward")

    def updateScreen0(self):
        guiRenderer = self.renderer
        gameNetworking = self.gameNetworking
        if guiRenderer.get_element("nameInput").text == "":
            guiRenderer.get_element("submitName").show = False

        else:
            guiRenderer.get_element("submitName").show = True

        if gameNetworking.uuid != "":
            self.screenMaster.screenID = 1

    def updateScreen1(self):
        guiRenderer = self.renderer
        screen = self.screen
        gameNetworking = self.gameNetworking

        try:
            if guiRenderer.get_element("gameNameInput").text != "" and int(guiRenderer.get_element("playerCountInput").text) >= 1:
                guiRenderer.get_element("gameSubmit").show = True

            else:
                guiRenderer.get_element("gameSubmit").show = False

        except ValueError:
            guiRenderer.get_element("gameSubmit").show = False

        if guiRenderer.get_element("gameName").renderables[0].text.text != "Choose a game":
            guiRenderer.get_element("joinButton").show = True

        else:
            guiRenderer.get_element("joinButton").show = False


        removeOffset = 0
        for i in range(len(self.uuids)):
            game_id = self.uuids[i-removeOffset]
            if game_id not in gameNetworking.games.keys():
                self.uuids.pop(i-removeOffset)
                guiRenderer.remove_element(f"gameListButton{game_id}")
                del self.uuidToButton[game_id]
                removeOffset += 1

        for uuid in gameNetworking.games.keys():
            if uuid not in self.uuids:
                self.uuids.append(uuid)
                gameNetworking.getName(gameNetworking.games[uuid]["host"])
                thisButton = GameButton(self.w+10, 0, uuid, (255, 255, 255), self.fontS, screen.get_width(), gameNetworking, guiRenderer)
                guiRenderer.add_element(thisButton, tag=f"gameListButton{uuid}")
                self.uuidToButton[uuid] = thisButton

        for index, uuid in enumerate(self.uuids):
            if self.gamePage * self.perPage <= index < (self.gamePage+1) * self.perPage:
                self.uuidToButton[uuid].show = True
                # print((self.w + 10, 200+56*(index-self.gamePage * self.perPage)))
                self.uuidToButton[uuid].moveTo(self.w + 10, 200+56*(index-self.gamePage * self.perPage))
                self.uuidToButton[uuid].renderables[0].color = (116, 213, 255) if index%2==1 else (255, 255, 255)

            else:
                self.uuidToButton[uuid].show = False

        if self.gamePage > 0:
            guiRenderer.get_element("pageBackward").show = True

        else:
            guiRenderer.get_element("pageBackward").show = False

        if self.gamePage < math.ceil(len(self.uuids)/self.perPage) - 1:
            guiRenderer.get_element("pageForward").show = True

        else:
            guiRenderer.get_element("pageForward").show = False

        guiRenderer.get_element("pageText").renderables[0].text.set_text(f"Page {self.gamePage+1}/{math.ceil(len(self.uuids)/self.perPage)}")

        if random.randint(1, 100) <= 10:
            newFlair = Flair(random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
            flairID = str(UUID.uuid4())
            guiRenderer.add_element(newFlair, tag=f"starFlair{flairID}")
            self.flairs.append(f"starFlair{flairID}")

        removeOffset = 0
        for x in range(len(self.flairs)):
            i = self.flairs[x-removeOffset]
            if guiRenderer.get_element(i).done:
                guiRenderer.remove_element(i)
                self.flairs.pop(x-removeOffset)
                removeOffset += 1

        if gameNetworking.gameUuid != "":
            self.screenMaster.screenID = 2

    def on_end_screen(self):
        guiRenderer = self.renderer
        destroy = ["loadingBanner", "statusText", "detailText"]
        for tag in destroy:
            self.renderer.remove_element(tag)

        guiRenderer.add_element(GuiElement(0, 0, [Renderable(loader.load_image("winbanner", size=self.screen.get_size()), (0, 0))]), tag="winbanner")
        times = []
        allPlayers = list(self.gameNetworking.gameData["gameData"]["playerHealth"])
        for player, time in self.gameNetworking.gameData["result"].items():
            times.append((player, time - self.gameNetworking.gameData["gameData"]["timeStart"]))
            allPlayers.remove(player)
            self.gameNetworking.getName(player)

        times.sort(key=lambda x:x[1], reverse=True)
        for index, item in enumerate(times):
            playerRanking = GuiElement(500, 200 + 50*index, [Renderable(Text("loading...", self.fontS, (0, 0, 0), (500, 200+50*index)))])
            self.gameEndUuids.append(item[0])
            guiRenderer.add_element(playerRanking, tag=f"gameEnd{item[0]}")

        numberOne = GuiElement(100, 500, [Renderable(Text("loading...", self.font, (0, 0, 0), (100, 500)))])
        self.gameNetworking.getName(allPlayers[0])
        guiRenderer.add_element(numberOne, tag="numberOne")

    def updateScreen3(self):
        guiRenderer = self.renderer
        if random.randint(1, 100) <= 10:
            newFlair = Flair(random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
            flairID = str(UUID.uuid4())
            guiRenderer.add_element(newFlair, tag=f"starFlair{flairID}")
            self.flairs.append(f"starFlair{flairID}")

        removeOffset = 0
        for x in range(len(self.flairs)):
            i = self.flairs[x-removeOffset]
            if guiRenderer.get_element(i).done:
                guiRenderer.remove_element(i)
                self.flairs.pop(x-removeOffset)
                removeOffset += 1

        times = []
        allPlayers = list(self.gameNetworking.gameData["gameData"]["playerHealth"])
        for player, time in self.gameNetworking.gameData["result"].items():
            times.append((player, time - self.gameNetworking.gameData["gameData"]["timeStart"]))
            allPlayers.remove(player)

        times.sort(key=lambda x:x[1], reverse=True)
        for index, item in enumerate(times):
            try:
                nameText = self.gameNetworking.uuidToName[item[0]]

            except KeyError:
                nameText = "loading..."
            guiRenderer.get_element(f"gameEnd{item[0]}").renderables[0].text.set_text(f"{index+1}. {nameText} - {item[1]} secs")

        try:
            nOneText = f"{self.gameNetworking.uuidToName[allPlayers[0]]}"

        except KeyError:
            nOneText = "loading..."

        guiRenderer.get_element("numberOne").renderables[0].text.set_text(nOneText)

    def on_loading_window(self):
        destroy = ["lightBlueBanner", "createBanner", "nameBanner", "gameNameInput", "playerCountBanner",
                   "playerCountInput", "lobbySepLine", "gameSubmit", "gameName", "passwordText", "passwordInput",
                   "playerList", "joinButton", "pageBackward", "pageText", "pageForward", "blueBanner", "gameLogo",
                   "musicBanner", "musicSlider", "sfxBanner", "sfxSlider"]
        for uuid in self.uuids:
            destroy.append(f"gameListButton{uuid}")

        self.uuids = []
        self.uuidToButton = {}
        for tag in destroy:
            self.renderer.remove_element(tag)

        loadingBanner = GuiElement(0, 0, [Renderable(loader.load_image("loadingBanner", size=self.screen.get_size()), (0, 0))])
        self.renderer.add_element(loadingBanner, tag="loadingBanner")
        statusText = GuiElement(10, 450, [Renderable(Text("Waiting for Players...", self.font, (193, 111, 0), (10, 450)))])
        self.renderer.add_element(statusText, tag="statusText")
        detailText = GuiElement(10, 500, [Renderable(Text("Details...", self.fontS, (0, 0, 0), (10, 500)))])
        self.renderer.add_element(detailText, tag="detailText")

    def updateScreen2(self):
        guiRenderer = self.renderer
        if random.randint(1, 100) <= 10:
            newFlair = Flair(random.randint(0, self.screen.get_width()), random.randint(0, self.screen.get_height()))
            flairID = str(UUID.uuid4())
            guiRenderer.add_element(newFlair, tag=f"starFlair{flairID}")
            self.flairs.append(f"starFlair{flairID}")

        removeOffset = 0
        for x in range(len(self.flairs)):
            i = self.flairs[x-removeOffset]
            if guiRenderer.get_element(i).done:
                guiRenderer.remove_element(i)
                self.flairs.pop(x-removeOffset)
                removeOffset += 1

        gameState = self.gameNetworking.gameStatus
        if gameState == "Pending":
            generalText = "Waiting for Players..."
            try:
                game = self.gameNetworking.games[self.gameNetworking.gameUuid]
                infoText = f"{len(game['players'])}/{game['settings']['maxPlayers']} players"

            except KeyError:
                infoText = "Unavailable, wait a sec..."

        elif gameState == "Loading":
            generalText = "Loading game..."
            infoText = "Game will be starting soon!"

        elif gameState == "Loaded":
            generalText = "Starting game..."
            infoText = "Get ready!"
            threading.Thread(target=self.gameInitalizer.startGame, daemon=True).start()

        else:
            generalText = "Unavailable"
            infoText = "Wait a sec..."

        guiRenderer.get_element("statusText").renderables[0].text.set_text(generalText)
        guiRenderer.get_element("detailText").renderables[0].text.set_text(infoText)
