import pygame
from pygame import gfxdraw
import random
from termcolor import colored
import pygamepopup
from pygamepopup.menu_manager import MenuManager
# menu_manager = MenuManager(screen)
from pygamepopup.components import Button, InfoBox
import time
import copy


class Jeu:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.popup = PopUp()


class PopUp:
    def __init__(self):
        self.menuManager = MenuManager()
        self.myCustomPopUp = InfoBox(
            "Fin du jeu", [Button(title="Quitter", callback=lambda:None)])

    def openPopUp(self, screen):
        self.menuManager.screen = screen
        self.menuManager.open_menu(self.myCustomPopUp)


pygame.init()
jeu = Jeu()
PopUp.openPopUp(jeu.screen)
