import pygame

import loader
from render.gui.SubmitButton import SubmitButton
from render.gui.base.element import GuiElement
from render.gui.base.renderable import Renderable
from render.gui.base.text import Text
from render.gui.elements.button import Button
from render.gui.elements.textinput import TextInput

def makeGui(guiRenderer, screen, gamenetworking, theFont, theFontS):
    w = screen.get_width()*0.381966011
    blueBanner = GuiElement(0, 0, [Renderable(pygame.Rect(0, 0, w, screen.get_height()), (0, 55, 165), 0)])
    guiRenderer.add_element(blueBanner, tag="blueBanner")
    gameLogo = GuiElement(10, 10, [Renderable(Text("gam", (loader.load_font("theFont", 72), 72), (255, 255, 255), (10, 10)))])
    guiRenderer.add_element(gameLogo, tag="gameLogo")
    nameInputBanner = GuiElement(10, 100, [Renderable(Text("Name:", theFont, (0, 0, 0), (10, 100)))])
    guiRenderer.add_element(nameInputBanner, tag="nameInputBanner")
    nameInput = TextInput(10, 150, Text("", theFont, (0, 0, 0), (10, 150)), maxLen=9)
    guiRenderer.add_element(nameInput, tag="nameInput")
    submitName = SubmitButton(10, 250, 200, 50, theFont, lambda:gamenetworking.join(nameInput.text) if nameInput.text != "" else None)
    guiRenderer.add_element(submitName, tag="submitName")

    lightBlueBanner = GuiElement(0, 0, [Renderable(pygame.Rect(w, 0, screen.get_width()-w, screen.get_height()), (174, 200, 255), 0)])
    lightBlueBanner.show = False
    guiRenderer.add_element(lightBlueBanner, tag="lightBlueBanner")
    createBanner = GuiElement(w+10, 10, [Renderable(Text("Create a Game", theFont, (255, 170, 0), (w+10, 10)))])
    createBanner.show = False
    guiRenderer.add_element(createBanner, tag="createBanner")
    nameBanner = GuiElement(w+10, 60, [Renderable(Text("Name:", theFontS, (0, 0, 0), (w+10, 60)))])
    nameBanner.show = False
    guiRenderer.add_element(nameBanner, tag="nameBanner")
    gameNameInput = TextInput(w+70, 60, Text("", theFontS, (0, 0, 0), (w+70, 60)), maxLen=18)
    gameNameInput.show = False
    guiRenderer.add_element(gameNameInput, tag="gameNameInput")
    playerCountBanner = GuiElement(w+350, 60, [Renderable(Text("Players:", theFontS, (0, 0, 0), (w+350, 60)))])
    playerCountBanner.show = False
    guiRenderer.add_element(playerCountBanner, tag="playerCountBanner")
    playerCountInput = TextInput(w+430, 60, Text("", theFontS, (0, 0, 0), (w+430, 60)), maxLen=1)
    playerCountInput.show = False
    guiRenderer.add_element(playerCountInput, tag="playerCountInput")
    sepLine = GuiElement(w+3, 125, [Renderable(pygame.Rect(w+3, 125, screen.get_width() - w - 6, 4), (0, 0, 0), 0)])
    sepLine.show = False
    guiRenderer.add_element(sepLine, tag="lobbySepLine")
    # TODO: Fix maxPlayers not sending
    gameSubmit = SubmitButton(w+10, 100, 100, 50, theFontS, lambda: gamenetworking.createGame(gameNameInput.text,
                                                                                              [("maxPlayers", int(playerCountInput.text))]))
    gameSubmit.show = False
    guiRenderer.add_element(gameSubmit, tag="gameSubmit")


