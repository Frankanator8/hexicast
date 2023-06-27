import math
import random
import threading
import time
import uuid as UUID
import pygame
import loader
from render import fonts
from render.gui.ExitButton import ExitButton
from render.gui.Flair import Flair
from render.gui.GameButton import GameButton
from render.gui.GamemodeButton import GamemodeButton
from render.gui.MapButton import MapButton
from render.gui.MapViewer import MapViewer
from render.gui.SubmitButton import SubmitButton
from render.gui.ToggleButton import ToggleButton
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button
from render.gui.elements.slider import Slider
from render.gui.elements.textinput import TextInput
from datetime import datetime

class GuiMaker:
    TIPS = [
        "Use WASD instead of arrow keys\nto move so you can cast\nspells while moving!",
        "When aiming, you can immediately\nstart casting the next\nspell when you click to aim!",
        "Explosion Propulsion can be\ncountered with Water by using\nthe river to detonate the bomb",
        "Rated challenges only provide\n1/2 of the rating change\na ladder game does",
        "Equal or higher tier spells will\ndestroy lower or equal\ntier spells"
    ]
    def __init__(self, screen, renderer, gameNetworking, screenMaster, gameInitializer, musicMaster, soundMaster):
        self.screen = screen
        self.gameNetworking = gameNetworking
        self.font = fonts.Fonts.font48
        self.fontM = fonts.Fonts.font36
        self.fontS = fonts.Fonts.font24
        self.fontXS = fonts.Fonts.font15
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

        self.tutorialStage = 0
        self.loginScreen = 0
        self.gameSelectScreen = 0

        self.mapButtons = []
        self.mapButtonIds = []
        self.mapViewer = None
        self.selectedMap = ""
        self.ladderTime = 0
        self.lastTime = time.time()

        self.flairs = []

    def incrementTutorial(self):
        self.tutorialStage += 1
        if self.tutorialStage >= 5:
            self.deleteTutorial()

        else:
            guiRenderer = self.renderer
            guiRenderer.get_element("bigTutorial").renderables[0].text.set_text(f"Tutorial {self.tutorialStage+1}/5")
            helpBanner = loader.load_image(f"tutorial/{self.tutorialStage}")
            helpBanner.set_alpha(210)
            guiRenderer.get_element("tutorialBanner").renderables[0].disp = helpBanner
            with open(f"assets/tutorial/{self.tutorialStage}.txt") as f:
                guiRenderer.get_element("tutorialText").renderables[0].text.set_text(f.read())

    def makeCredits(self):
        self.deleteCredits()
        self.deleteTutorial()
        guiRenderer = self.renderer
        creditBanner = loader.load_image("credits")
        creditBanner.set_alpha(210)
        banner = GuiElement(100, 75, [Renderable(creditBanner, (100, 75))])
        guiRenderer.add_element(banner, tag="creditsBanner")
        bigCredit = GuiElement(110, 95, [Renderable(Text("Credits", self.font, (255, 255, 255), (110, 95)))])
        guiRenderer.add_element(bigCredit, tag="bigCredit")
        with open("assets/credits.txt") as f:
            creditText = GuiElement(110, 135, [Renderable(Text(f.read(), self.fontS, (255, 255, 255), (110, 135)))])
        guiRenderer.add_element(creditText, tag="creditText")
        exit = Button(635, 95, [Renderable(loader.load_image("exit"), (635, 95))], lambda:None, lambda:None, lambda:None, self.deleteCredits)
        guiRenderer.add_element(exit, tag="exitCredits")

    def deleteCredits(self):
        guiRenderer = self.renderer
        destroy = ["creditsBanner", "bigCredit", "creditText", "exitCredits"]
        for tag in destroy:
            if guiRenderer.has_element(tag):
                guiRenderer.remove_element(tag)

    def makeTutorial(self):
        self.deleteTutorial()
        self.deleteCredits()
        guiRenderer = self.renderer
        helpBanner = loader.load_image(f"tutorial/{self.tutorialStage}")
        helpBanner.set_alpha(210)
        banner = GuiElement(100, 75, [Renderable(helpBanner, (100, 75))])
        guiRenderer.add_element(banner, tag="tutorialBanner")
        bigTutorial = GuiElement(110, 95, [Renderable(Text(f"Tutorial {self.tutorialStage+1}/5", self.font, (255, 255, 255), (110, 95)))])
        guiRenderer.add_element(bigTutorial, tag="bigTutorial")
        with open(f"assets/tutorial/{self.tutorialStage}.txt") as f:
            tutorialText = GuiElement(110, 135, [Renderable(Text(f.read(), self.fontXS, (255, 255, 255), (110, 135)))])
        guiRenderer.add_element(tutorialText, tag="tutorialText")
        exit = Button(635, 95, [Renderable(loader.load_image("exit"), (635, 95))], lambda:None, lambda:None, lambda:None, self.deleteTutorial)
        guiRenderer.add_element(exit, tag="exitTutorial")
        next = Button(635, 490, [Renderable(loader.load_image("arrowF"), (635, 490))], lambda:None, lambda:None, lambda:None, self.incrementTutorial)
        guiRenderer.add_element(next, tag="nextTutorial")

    def deleteTutorial(self):
        guiRenderer = self.renderer
        self.tutorialStage = 0
        destroy = ["tutorialBanner", "bigTutorial", "tutorialText", "exitTutorial", "nextTutorial"]
        for tag in destroy:
            if guiRenderer.has_element(tag):
                guiRenderer.remove_element(tag)

    def makeLogin(self):
        self.loginScreen = 1
        guiRenderer = self.renderer
        delete = ["login", "nameInputBanner", "nameInput", "submitName"]
        for tag in delete:
            guiRenderer.remove_element(tag)

        usernameBanner = GuiElement(10, 100, [Renderable(Text("Username", self.fontS, (0, 0, 0), (10, 100)))])
        guiRenderer.add_element(usernameBanner, tag="usernameBanner")
        usernameInput = TextInput(10, 130, Text("", self.fontS, (0, 0, 0), (10, 130)), maxLen=18)
        guiRenderer.add_element(usernameInput, tag="usernameInput")

        passwordBanner = GuiElement(10, 170, [Renderable(Text("Password", self.fontS, (0, 0, 0), (10, 170)))])
        guiRenderer.add_element(passwordBanner, tag="passwordBanner")
        passwordInput = TextInput(10, 200, Text("", self.fontS, (0, 0, 0), (10, 200)), maxLen=18, subchar="*")
        guiRenderer.add_element(passwordInput, tag="passwordInput")

        loginButton = SubmitButton(10, 250, 100, 30, self.fontS, lambda:self.gameNetworking.login(usernameInput.text, passwordInput.text), text="Log in")
        guiRenderer.add_element(loginButton, tag="loginButton")
        helpText = GuiElement(120, 250, [Renderable(Text("", self.fontS, (255, 0, 0), (120, 250)))])
        guiRenderer.add_element(helpText, tag="helpText")

        signupBanner = GuiElement(10, 290, [Renderable(Text("Don't have an account?", self.fontS, (0, 0, 0), (10, 290)))])
        guiRenderer.add_element(signupBanner, tag="signupBanner")

        signupButton = SubmitButton(10, 320, 100, 30, self.fontS, self.makeSignup, text="Sign Up")
        guiRenderer.add_element(signupButton, tag="signupButton")

    def makeSignup(self):
        self.loginScreen = 2
        guiRenderer = self.renderer
        delete = ["usernameBanner", "usernameInput",
                  "passwordBanner", "passwordInput", "loginButton", "signupBanner", "signupButton", "helpText"]
        for tag in delete:
            guiRenderer.remove_element(tag)

        usernameBanner = GuiElement(10, 100, [Renderable(Text("Username", self.fontS, (0, 0, 0), (10, 100)))])
        guiRenderer.add_element(usernameBanner, tag="usernameBanner")
        usernameInput = TextInput(10, 130, Text("", self.fontS, (0, 0, 0), (10, 130)), maxLen=18)
        guiRenderer.add_element(usernameInput, tag="usernameInput")

        displayNameBanner = GuiElement(10, 170, [Renderable(Text("Display Name", self.fontS, (0, 0, 0), (10, 170)))])
        guiRenderer.add_element(displayNameBanner, tag="displayNameBanner")
        displayNameInput = TextInput(10, 200, Text("", self.fontS, (0, 0, 0), (10, 200)), maxLen=18)
        guiRenderer.add_element(displayNameInput, tag="displayNameInput")

        passwordBanner = GuiElement(10, 240, [Renderable(Text("Password (Aa alphabet and space)", self.fontS, (0, 0, 0), (10, 240)))])
        guiRenderer.add_element(passwordBanner, tag="passwordBanner")
        passwordInput = TextInput(10, 270, Text("", self.fontS, (0, 0, 0), (10, 270)), maxLen=18, subchar="*")
        guiRenderer.add_element(passwordInput, tag="passwordInput")

        passwordViewer = Button(10, 310, [Renderable(pygame.Rect(10, 310, 130, 20), (255, 79, 79), 2),
                                          Renderable(Text("Hover to view password", self.fontXS, (0, 0, 0), (10, 310)))],
                                lambda:guiRenderer.get_element("passwordInput").setSubchar(""),
                                lambda:guiRenderer.get_element("passwordInput").setSubchar("*"),
                                lambda:None,
                                lambda:None)
        guiRenderer.add_element(passwordViewer, tag="passwordViewer")

        signupButton = SubmitButton(10, 340, 200, 50, self.font, lambda:self.gameNetworking.signup(usernameInput.text, displayNameInput.text, passwordInput.text), text="Sign Up!")
        guiRenderer.add_element(signupButton, tag="signupButton")

        helpText = GuiElement(110, 100, [Renderable(Text("", self.fontS, (255, 0, 0), (110, 100)))])
        guiRenderer.add_element(helpText, tag="helpText")

    def updateScreen0(self):
        guiRenderer = self.renderer
        gameNetworking = self.gameNetworking
        if self.loginScreen == 0:
            if guiRenderer.get_element("nameInput").text == "":
                guiRenderer.get_element("submitName").show = False

            else:
                guiRenderer.get_element("submitName").show = True

        elif self.loginScreen == 1:
            if guiRenderer.get_element("usernameInput").text != "" and guiRenderer.get_element("passwordInput").text != "":
                guiRenderer.get_element("loginButton").show = True

            else:
                guiRenderer.get_element("loginButton").show = False

            guiRenderer.get_element("helpText").renderables[0].text.set_text(self.gameNetworking.signinMessage)

        elif self.loginScreen == 2:
            if guiRenderer.get_element("usernameInput").text != "" and guiRenderer.get_element("passwordInput").text != "" \
                    and guiRenderer.get_element("displayNameInput").text != "":
                guiRenderer.get_element("signupButton").show = True

            else:
                guiRenderer.get_element("signupButton").show = False

            guiRenderer.get_element("helpText").renderables[0].text.set_text(self.gameNetworking.signinMessage)


        if gameNetworking.uuid != "":
            self.screenMaster.screenID = 1

    def makeInitialGui(self):
        guiRenderer = self.renderer

        blueBanner = GuiElement(0, 0, [Renderable(loader.load_image("sidebanner", size=(self.w, self.screen.get_height())), (0, 0))])
        guiRenderer.add_element(blueBanner, tag="blueBanner")
        aestheticBanner = GuiElement(self.w, 0, [Renderable(loader.load_image("back", size=(self.screen.get_width()-self.w, self.screen.get_height())), (self.w, 0))])
        guiRenderer.add_element(aestheticBanner, tag="aestheticBanner")
        gameLogo = GuiElement(0, 10, [Renderable(loader.load_image("logo", size=(self.w,80)), (0, 10))])
        guiRenderer.add_element(gameLogo, tag="gameLogo")
        login = SubmitButton(10, 110, 280, 75, self.font, self.makeLogin, text="Log in/Sign Up")
        guiRenderer.add_element(login, tag="login")
        nameInputBanner = GuiElement(10, 200, [Renderable(Text("or with guest name:", self.fontS, (0, 0, 0), (10, 200)))])
        guiRenderer.add_element(nameInputBanner, tag="nameInputBanner")
        nameInput = TextInput(10, 225, Text("", self.fontS, (0, 0, 0), (10, 225)), maxLen=18)
        guiRenderer.add_element(nameInput, tag="nameInput")
        submitName = SubmitButton(10, 275, 200, 50, self.font, lambda:self.gameNetworking.join(nameInput.text) if nameInput.text != "" else None)
        guiRenderer.add_element(submitName, tag="submitName")

        musicBanner = GuiElement(10, self.screen.get_height()-200, [Renderable(Text("Music Volume", self.fontS, (0, 0, 0), (10, self.screen.get_height()-200)))])
        guiRenderer.add_element(musicBanner, tag="musicBanner")
        musicSlider = Slider(10, self.screen.get_height()-170, self.w-20, 20, 100, lambda x:self.musicMaster.set_volume(x/100))
        guiRenderer.add_element(musicSlider, tag="musicSlider")
        sfxBanner = GuiElement(10, self.screen.get_height()-140, [Renderable(Text("Sound FX Volume", self.fontS, (0, 0, 0), (10, self.screen.get_height()-140)))])
        guiRenderer.add_element(sfxBanner, tag="sfxBanner")
        sfxSlider = Slider(10, self.screen.get_height()-110, self.w-20, 20, 100, lambda x:self.soundMaster.set_volume(x/100))
        guiRenderer.add_element(sfxSlider, tag="sfxSlider")

        credits = SubmitButton(10, self.screen.get_height() - 70, 120, 50, self.fontM, self.makeCredits, text="Credits")
        guiRenderer.add_element(credits, tag="creditButton")
        credits = SubmitButton(150, self.screen.get_height() - 70, 140, 50, self.fontM, self.makeTutorial, text="Tutorial")
        guiRenderer.add_element(credits, tag="tutorialButton")

    def decrementPage(self):
        if self.gamePage > 0:
            self.gamePage -= 1

    def incrementPage(self):
        if self.gamePage < math.ceil(len(self.uuids)/self.perPage) - 1:
            self.gamePage += 1

    def deleteSelectScreen0(self):
        guiRenderer = self.renderer
        delete = ["ladderButton", "challengeButton", "privateButton", "playerIcon", "dispName", "userName", "trophyIcon",
                  "trophyText", "dateIcon", "dateText", "sepLine", "gameModeText"]
        for tag in delete:
            if guiRenderer.has_element(tag):
                guiRenderer.remove_element(tag)

    def createChallengeGUI(self):
        guiRenderer = self.renderer
        self.deleteSelectScreen0()

        self.gameSelectScreen = 2

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
        ratedButton = ToggleButton(self.w+350, 95, "Rated")
        guiRenderer.add_element(ratedButton, tag="ratedButton")
        gameSubmit = SubmitButton(self.w+10, 100, 100, 50, self.fontS, lambda: self.gameNetworking.createGame(gameNameInput.text,
                                                                                                              {"maxPlayers": int(playerCountInput.text), "rated":ratedButton.value, "show":True, "type":"challenge"}))

        guiRenderer.add_element(gameSubmit, tag="gameSubmit")

        gameName = GuiElement(10, 100, [Renderable(Text("Choose a game", self.font, (5, 0, 149), (10, 100)))])
        guiRenderer.add_element(gameName, tag="gameName")
        playerList = GuiElement(10, 170, [Renderable(Text("Players:", self.fontS, (5, 0, 149), (10, 170)))])
        guiRenderer.add_element(playerList, tag="playerList")
        join = SubmitButton(10, 260, 200, 75, self.font, self.gameNetworking.joinGame, text="Join!")
        guiRenderer.add_element(join, tag="joinButton")

        pageForward = Button(self.w+10, 150, [Renderable(loader.load_image("arrowB"), (self.w+10, 150))], lambda:None, lambda:None, lambda:None, self.decrementPage)
        guiRenderer.add_element(pageForward, tag="pageBackward")
        pageText = GuiElement(self.w+40, 150, [Renderable(Text("Page", self.fontS, (255, 255, 255), (self.w+40, 150)))])
        guiRenderer.add_element(pageText, tag="pageText")
        pageForward = Button(self.w+150, 150, [Renderable(loader.load_image("arrowF"), (self.w+150, 150))], lambda:None, lambda:None, lambda:None, self.incrementPage)
        guiRenderer.add_element(pageForward, tag="pageForward")

        backButton = Button(self.screen.get_width() - 150, 10, [Renderable(loader.load_image("exit", size=(25, 25)), (self.screen.get_width() - 150, 10)),
                                                                Renderable(Text("Back to menu", self.fontS, (0, 0, 0), (self.screen.get_width() - 120, 10)))],
                            lambda:backButton.renderables[1].text.set_color((255, 255, 255)), lambda:backButton.renderables[1].text.set_color((0, 0, 0)), lambda:None, self.create_selectscreen0)
        guiRenderer.add_element(backButton, tag="backButton")

    def createPrivateGUI(self):
        self.deleteSelectScreen0()
        self.gameSelectScreen = 3
        guiRenderer = self.renderer

        joinText = GuiElement(self.w+10, 60, [Renderable(Text("Got a code? Input it here:", self.font, (0, 0, 0), (self.w+10, 60)))])
        guiRenderer.add_element(joinText, tag="joinText")
        joinInput = TextInput(self.w+10, 110, Text("", self.fontM, (0, 0, 0), (self.w+10, 110)))
        guiRenderer.add_element(joinInput, tag="joinInput")
        joinButton = SubmitButton(self.w+10, 165, 100, 20, self.fontS, lambda:self.gameNetworking.joinPrivateGame(joinInput.text), text="Join")
        guiRenderer.add_element(joinButton, tag="joinButton")
        joinError = GuiElement(self.w+120, 165, [Renderable(Text("", self.fontS, (255, 0, 0), (self.w+120, 165)))])
        guiRenderer.add_element(joinError, tag="joinError")

        createText = GuiElement(self.w+10, 180, [Renderable(Text("...or create a game", self.fontM, (0, 0, 0), (self.w+10, 180)))])
        guiRenderer.add_element(createText, tag="createText")

        playerCountBanner = GuiElement(self.w+10, 240, [Renderable(Text("Players:", self.fontS, (0, 0, 0), (self.w+10, 240)))])
        guiRenderer.add_element(playerCountBanner, tag="playerCountBanner")
        playerCountInput = TextInput(self.w+90, 240, Text("", self.fontS, (0, 0, 0), (self.w+90, 240)), maxLen=1)
        guiRenderer.add_element(playerCountInput, tag="playerCountInput")

        nameBanner = GuiElement(self.w+150, 240, [Renderable(Text("Code:", self.fontS, (0, 0, 0), (self.w+150, 240)))])
        guiRenderer.add_element(nameBanner, tag="nameBanner")
        gameNameInput = TextInput(self.w+200, 240, Text("", self.fontS, (0, 0, 0), (self.w+200, 240)), maxLen=18)
        guiRenderer.add_element(gameNameInput, tag="gameNameInput")

        mapText = GuiElement(self.w+10, 300, [Renderable(Text("Choose a map (hover to preview)", self.fontM, (0, 0, 0), (self.w+10, 300)))])
        guiRenderer.add_element(mapText, tag="mapText")
        self.mapViewer = MapViewer(self.w+170, 350, self.screen.get_width()-(self.w+170)-20, 200)
        guiRenderer.add_element(self.mapViewer, tag="mapViewer")
        self.mapButtons = []
        self.mapButtonIds = []
        for index, map in enumerate(self.gameNetworking.mapInfo):
            mapName, mapInfo = map
            mapButton = MapButton(self.w+10, 350+index*28, 150, 25, mapName, mapInfo, self.mapViewer, self.mapButtons)
            self.mapButtons.append(mapButton)
            guiRenderer.add_element(mapButton, tag=f"mapButton{mapName}")
            self.mapButtonIds.append(f"mapButton{mapName}")
        gameSubmit = SubmitButton(self.w+10, 550, 100, 40, self.fontS, lambda: self.gameNetworking.createPrivateGame(gameNameInput.text,
                                                                                                              {"maxPlayers": int(playerCountInput.text), "rated":False, "map":self.selectedMap, "show":False, "type":"private"}))
        guiRenderer.add_element(gameSubmit, tag="gameSubmit")

        gameSubmitError = GuiElement(self.w+120, 560, [Renderable(Text("", self.fontS, (255, 0, 0), (self.w+120, 560)))])
        guiRenderer.add_element(gameSubmitError, tag="gameSubmitError")


        backButton = Button(self.screen.get_width() - 150, 10, [Renderable(loader.load_image("exit", size=(25, 25)), (self.screen.get_width() - 150, 10)),
                                                                Renderable(Text("Back to menu", self.fontS, (0, 0, 0), (self.screen.get_width() - 120, 10)))],
                            lambda:backButton.renderables[1].text.set_color((255, 255, 255)), lambda:backButton.renderables[1].text.set_color((0, 0, 0)), lambda:None, self.create_selectscreen0)
        guiRenderer.add_element(backButton, tag="backButton")

    def createLadderGUI(self):
        self.deleteSelectScreen0()
        self.gameSelectScreen = 1
        self.ladderTime = 0
        guiRenderer = self.renderer

        joiningText = GuiElement(self.w+10, 100, [Renderable(Text("Finding an opponent...", self.font, (255, 195, 75), (self.w+10, 100)))])
        guiRenderer.add_element(joiningText, tag="joiningText")

        tipText = GuiElement(self.w+10, 200, [Renderable(Text(random.choice(self.TIPS), self.fontM, (0, 0, 0), (self.w+10, 200)))])
        guiRenderer.add_element(tipText, tag="tipText")

    def resetSelectWindow(self):
        destroy = ["createBanner", "nameBanner", "gameNameInput", "playerCountBanner",
                   "playerCountInput", "lobbySepLine", "gameSubmit", "gameName",
                   "playerList", "joinButton", "pageBackward", "pageText", "pageForward", "backButton", "ratedButton",

                   "joinText", "joinInput", "createText", "mapText", "mapViewer", "gameSubmitError", "joinError",

                   "joiningText", "tipText"]
        destroy.extend(self.mapButtonIds)
        for uuid in self.uuids:
            destroy.append(f"gameListButton{uuid}")

        self.uuids = []
        self.uuidToButton = {}
        for tag in destroy:
            if self.renderer.has_element(tag):
                self.renderer.remove_element(tag)

    def doLadder(self):
        self.createLadderGUI()
        self.gameNetworking.queue()

    def create_selectscreen0(self):
        self.gameSelectScreen = 0
        self.resetSelectWindow()
        guiRenderer = self.renderer
        lightBlueBanner = GuiElement(0, 0, [Renderable(loader.load_image("lobbyBanner", size=(self.screen.get_width()-self.w, self.screen.get_height())), (self.w, 0))])
        guiRenderer.add_element(lightBlueBanner, tag="lightBlueBanner")

        ladderButton = GamemodeButton(self.w+10, 200, self.screen.get_width()-(self.w+10)-10, 100, GamemodeButton.LADDER, self.gameNetworking, self.doLadder)
        guiRenderer.add_element(ladderButton, tag="ladderButton")

        challengeButton = GamemodeButton(self.w+10, 320, self.screen.get_width()-(self.w+10)-10, 100, GamemodeButton.CHALLENGE, self.gameNetworking, self.createChallengeGUI)
        guiRenderer.add_element(challengeButton, tag="challengeButton")

        privateButton = GamemodeButton(self.w+10, 440, self.screen.get_width()-(self.w+10)-10, 100, GamemodeButton.PRIVATE, self.gameNetworking, self.createPrivateGUI)
        guiRenderer.add_element(privateButton, tag="privateButton")

        icon = GuiElement(self.w+10, 20, [Renderable(loader.load_image("p1/e", size=(100, 100)), (self.w+10, 20))])
        guiRenderer.add_element(icon, tag="playerIcon")

        dispName = GuiElement(self.w+110, 20, [Renderable(Text("loading...", self.font, (0, 0, 0), (self.w+110, 20)))])
        guiRenderer.add_element(dispName, tag="dispName")

        userName = GuiElement(self.w+110, 65, [Renderable(Text("loading...", self.fontS, (0, 0, 0), (self.w+110, 65)))])
        guiRenderer.add_element(userName, tag="userName")

        trophyIcon = GuiElement(self.w+110, 95, [Renderable(loader.load_image("trophy", size=(20, 20)), (self.w+110, 95))])
        guiRenderer.add_element(trophyIcon, tag="trophyIcon")
        trophyText = GuiElement(self.w+135, 95, [Renderable(Text("loading...", self.fontS, (0, 0, 0), (self.w+135, 95)))])
        guiRenderer.add_element(trophyText, tag="trophyText")

        dateIcon = GuiElement(self.w+220, 95, [Renderable(loader.load_image("calendar", size=(20, 20)), (self.w+220, 95))])
        guiRenderer.add_element(dateIcon, tag="dateIcon")
        dateText = GuiElement(self.w+245, 95, [Renderable(Text("loading...", self.fontS, (0, 0, 0), (self.w+245, 95)))])
        guiRenderer.add_element(dateText, tag="dateText")

        sepLine = GuiElement(self.w+10, 130, [Renderable(pygame.Rect(self.w+10, 130, self.screen.get_width()-self.w-20, 5), (0, 0, 0), 0)])
        guiRenderer.add_element(sepLine, tag="sepLine")

        gameModeText = GuiElement(self.w+10, 140, [Renderable(Text("Choose a gamemode:", self.font, (0, 0, 0), (self.w+10, 140)))])
        guiRenderer.add_element(gameModeText, tag="gameModeText")

    def on_game_select_window(self):
        self.gameSelectScreen = 0
        guiRenderer = self.renderer
        delete = ["nameInputBanner", "aestheticBanner", "nameInput", "submitName", "login", "usernameBanner", "usernameInput",
                  "passwordBanner", "passwordInput", "loginButton", "signupBanner", "signupButton", "displayNameBanner", "displayNameInput",
                  "passwordViewer", "signupButton", "helpText"]
        for tag in delete:
            if guiRenderer.has_element(tag):
                guiRenderer.remove_element(tag)


        if not guiRenderer.has_element("blueBanner"):
            blueBanner = GuiElement(0, 0, [Renderable(loader.load_image("sidebanner", size=(self.w, self.screen.get_height())), (0, 0))])
            guiRenderer.add_element(blueBanner, tag="blueBanner")
            gameLogo = GuiElement(0, 10, [Renderable(loader.load_image("logo", size=(self.w,80)), (0, 10))])
            guiRenderer.add_element(gameLogo, tag="gameLogo")
            musicBanner = GuiElement(10, self.screen.get_height()-200, [Renderable(Text("Music Volume", self.fontS, (0, 0, 0), (10, self.screen.get_height()-200)))])
            guiRenderer.add_element(musicBanner, tag="musicBanner")
            musicSlider = Slider(10, self.screen.get_height()-170, self.w-20, 20, self.musicMaster.volume*100, lambda x:self.musicMaster.set_volume(x/100))
            guiRenderer.add_element(musicSlider, tag="musicSlider")
            sfxBanner = GuiElement(10, self.screen.get_height()-140, [Renderable(Text("Sound FX Volume", self.fontS, (0, 0, 0), (10, self.screen.get_height()-140)))])
            guiRenderer.add_element(sfxBanner, tag="sfxBanner")
            sfxSlider = Slider(10, self.screen.get_height()-110, self.w-20, 20, self.soundMaster.volume * 100, lambda x:self.soundMaster.set_volume(x/100))
            guiRenderer.add_element(sfxSlider, tag="sfxSlider")

            credits = SubmitButton(10, self.screen.get_height() - 70, 120, 50, self.fontM, self.makeCredits, text="Credits")
            guiRenderer.add_element(credits, tag="creditButton")
            credits = SubmitButton(150, self.screen.get_height() - 70, 140, 50, self.fontM, self.makeTutorial, text="Tutorial")
            guiRenderer.add_element(credits, tag="tutorialButton")

        if guiRenderer.has_element("exitButton"):
            destroy = ["winbanner", "numberOne", "exitButton"]
            for i in self.gameEndUuids:
                destroy.append(f"gameEnd{i}")
            self.gameEndUuids = []
            for tag in destroy:
                guiRenderer.remove_element(tag)

        self.create_selectscreen0()


        self.deleteCredits()
        self.deleteTutorial()

    def mixColor(self, color1, color2, proportion):
        return (color1[0] * proportion + color2[0] * (1-proportion),
                color1[1] * proportion + color2[1] * (1-proportion),
                color1[2] * proportion + color2[2] * (1-proportion))

    def updateScreen1(self):
        guiRenderer = self.renderer
        screen = self.screen
        gameNetworking = self.gameNetworking
        if self.gameSelectScreen == 0:
            if gameNetworking.accountUuid != "":
                gameNetworking.getUserInfo(gameNetworking.accountUuid, uuid=True)
            gameNetworking.getName(gameNetworking.uuid)

            if self.gameNetworking.accountUuid == "":
                try:
                    dispText = gameNetworking.uuidToName[gameNetworking.uuid]

                except KeyError:
                    dispText = "loading..."

                usernameText = "You are playing as a guest."
                guiRenderer.get_element("trophyIcon").show = False
                guiRenderer.get_element("trophyText").show = False
                guiRenderer.get_element("dateIcon").show = False
                guiRenderer.get_element("dateText").show = False


            else:
                try:
                    userData = gameNetworking.userData[gameNetworking.accountUuid]
                    dispText = userData["displayName"]
                    usernameText = f"@{userData['username']}"
                    guiRenderer.get_element("trophyText").renderables[0].text.set_text(str(userData["rating"]))
                    guiRenderer.get_element("dateText").renderables[0].text.set_text(f"Joined {datetime.fromtimestamp(userData['joined']).strftime('%m/%d/%Y, %H:%M:%S')}")

                except KeyError:
                    dispText = "loading..."
                    usernameText = "loading..."

            guiRenderer.get_element("dispName").renderables[0].text.set_text(dispText)
            guiRenderer.get_element("userName").renderables[0].text.set_text(usernameText)

        elif self.gameSelectScreen == 1:
            self.ladderTime += time.time() - self.lastTime
            if self.ladderTime > 3:
                self.ladderTime = 0
                guiRenderer.get_element("tipText").renderables[0].text.set_text(random.choice(self.TIPS))

            guiRenderer.get_element("joiningText").renderables[0].text.set_color(self.mixColor((255, 195, 75), (255, 59, 59), (math.cos(self.ladderTime/3*math.pi*2)+1)/2))


        elif self.gameSelectScreen == 2:
            try:
                if guiRenderer.get_element("gameNameInput").text != "" and int(guiRenderer.get_element("playerCountInput").text) >= 2:
                    guiRenderer.get_element("gameSubmit").show = True

                else:
                    guiRenderer.get_element("gameSubmit").show = False

            except ValueError:
                guiRenderer.get_element("gameSubmit").show = False


            if guiRenderer.get_element("gameName").renderables[0].text.text != "Choose a game":
                guiRenderer.get_element("joinButton").show = True

            else:
                guiRenderer.get_element("joinButton").show = False

            if gameNetworking.accountUuid == "":
                guiRenderer.get_element("ratedButton").show = False


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
                    if not (gameNetworking.games[uuid]["settings"]["rated"] and gameNetworking.accountUuid == ""):
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

        elif self.gameSelectScreen == 3:
            for mapButton in self.mapButtons:
                if mapButton.selected:
                    self.selectedMap = mapButton.mapName

            try:
                if self.selectedMap != "" and guiRenderer.get_element("gameNameInput").text != "" and int(guiRenderer.get_element("playerCountInput").text) >= 2:
                    guiRenderer.get_element("gameSubmit").show = True

                else:
                    guiRenderer.get_element("gameSubmit").show = False

            except ValueError:
                guiRenderer.get_element("gameSubmit").show = False

            if guiRenderer.get_element("joinInput").text != "":
                guiRenderer.get_element("joinButton").show = True

            else:
                guiRenderer.get_element("joinButton").show = False

            guiRenderer.get_element("gameSubmitError").renderables[0].text.set_text(gameNetworking.createPrivateGameMessage)
            guiRenderer.get_element("joinError").renderables[0].text.set_text(gameNetworking.joinPrivateGameMessage)

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

        self.lastTime = time.time()

    def on_end_screen(self):
        guiRenderer = self.renderer
        destroy = ["loadingBanner", "statusText", "detailText"]
        for tag in destroy:
            self.renderer.remove_element(tag)

        guiRenderer.add_element(GuiElement(0, 0, [Renderable(loader.load_image("winbanner", size=self.screen.get_size()), (0, 0))]), tag="winbanner")
        times = []
        allPlayers = self.gameNetworking.gameData["players"]
        for player, time in self.gameNetworking.gameData["result"].items():
            times.append((player, time - self.gameNetworking.gameData["gameData"]["timeStart"]))
            allPlayers.remove(player)
            self.gameNetworking.getName(player)

        times.sort(key=lambda x:x[1], reverse=True)
        for index, item in enumerate(times):
            playerRanking = GuiElement(500, 175 + 50*index, [Renderable(Text("loading...", self.fontS, (255, 196, 85), (500, 175+50*index)))])
            self.gameEndUuids.append(item[0])
            guiRenderer.add_element(playerRanking, tag=f"gameEnd{item[0]}")

        numberOne = GuiElement(100, 500, [Renderable(Text("loading...", self.font, (0, 0, 0), (100, 500)))])
        self.gameNetworking.getName(allPlayers[0])
        guiRenderer.add_element(numberOne, tag="numberOne")

        exitButton = ExitButton(650, 525, self.gameInitalizer, self.screenMaster)
        guiRenderer.add_element(exitButton, tag="exitButton")

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
            times.append((player, round(time - self.gameNetworking.gameData["gameData"]["timeStart"], 1)))
            allPlayers.remove(player)

        times.sort(key=lambda x:x[1], reverse=True)
        for index, item in enumerate(times):
            try:
                nameText = self.gameNetworking.uuidToName[item[0]]

            except KeyError:
                nameText = "loading..."
            guiRenderer.get_element(f"gameEnd{item[0]}").renderables[0].text.set_text(f"{index+2}. {nameText} - {item[1]} secs")

        try:
            nOneText = f"{self.gameNetworking.uuidToName[allPlayers[0]]}"

        except KeyError:
            nOneText = "loading..."

        guiRenderer.get_element("numberOne").renderables[0].text.set_text(nOneText)

    def on_loading_window(self):
        self.deleteCredits()
        self.deleteTutorial()
        destroy = ["lightBlueBanner", "blueBanner", "gameLogo",
                   "musicBanner", "musicSlider", "sfxBanner", "sfxSlider", "creditButton", "tutorialButton"]
        self.resetSelectWindow()
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
