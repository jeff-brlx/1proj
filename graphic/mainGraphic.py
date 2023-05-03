import pygame
from pygame import gfxdraw
import random
from termcolor import colored
import pygamepopup
from pygamepopup.menu_manager import MenuManager
from pygamepopup.components import Button, InfoBox
import time
import copy
import sys


class case:
    def __init__(self):
        self.nature = 70

    def checkNature(self):
        # check la nature des cases (chemin,pion,barrière réelle, barrière parasite)
        #  et les affiche
        if self.nature == 0:
            return "00"
        if self.nature == 1:
            return "01"  # barrières horizontales   "-" non placées
        if self.nature == 2:
            return "02"  # barrières verticales     "|" non placées
        if self.nature == 10:
            return "10"  # barrières horizontales   "-" placées
        if self.nature == 20:
            return "20"  # barrières verticales     "|" placées
        if self.nature == 4:
            return "04"  # pion joueur 1
        if self.nature == 5:
            return "05"  # pion joueur 2
        if self.nature == 6:
            return "06"  # pion joueur 3
        if self.nature == 8:
            return "08"  # pion joueur 4
        if self.nature == 7:
            return "07"  # barrières parasite

    def getNature(self):
        return self.nature

    def setNature(self, newNature):
        self.nature = newNature


class jeu:

    def __init__(self):

        self.whiteSmoke = (247, 241, 233)
        self.whitheSmoke2 = (214, 214, 214)
        self.blue = (15, 116, 167)
        self.darkBlue = (0, 74, 112)
        self.gray = (150, 150, 150)
        self.gray2 = (66, 66, 66)
        self.black = (51, 51, 51)
        self.beige = (244, 205, 150)
        self.Red = (115, 33, 36)
        self.darkRed = (81, 13, 15)
        self.Brown = (115, 76, 71)
        self.lightBrown = (159, 104, 75)
        self.white = (247, 241, 233)
        self.orange = (255, 33, 0)
        self.darkOrange = (165, 22, 3)
        self.yellow = (245, 176, 39)
        self.darkYellow = (175, 116, 7)
        self.pink = (237, 20, 125)
        self.darkPink = (165, 0, 80)
        self.beige6 = (197, 173, 151)
        self.black2 = (29, 29, 31)
        self.beige3 = (245, 245, 220)
        self.green = (52, 168, 83)
        self.darkGreen = (26, 81, 41)
        self.golden1 = (199, 134, 12)
        self.golden2 = (245, 176, 39)
        self.gray = (214, 214, 214)
        self.gray3 = (188, 186, 186)

        self.clock = pygame.time.Clock()
        self.nbPlayers = None
        while self.nbPlayers not in [2, 3, 4]:
            try:
                self.nbPlayers = int(
                    input("Enter the number of players ( 2 , 3 or 4): "))
                if self.nbPlayers not in [2, 3, 4]:
                    print("Invalid input. Please enter a number between 2 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 2 and 4.")

        # Création d'un dictionnaire pour stocker les informations sur chaque joueur
        self.infosPlayers = {}
        print(" *  only 1 bot per game is tolered  * ")
        # Demander à l'utilisateur si chaque joueur est un bot ou un joueur réel
        for i in range(self.nbPlayers):
            player = "player " + str(i+1)
            nature = input("is "+player+" a bot ? (Yes/No)").lower()

            # Vérifier que l'utilisateur a entré une réponse valide
            while nature not in ["yes", "no"]:
                print("Invalid response . Please respond by Yes or No.")
                nature = input("is "+player+" a bot ? (Yes/No)").lower()

            # Stocker les informations sur chaque joueur dans le dictionnaire
            self.infosPlayers[player] = {
                "nature": "bot" if nature == "yes" else "human"}

        self.currentPlayer = random.randint(1, self.nbPlayers)

        self.gridSize = None
        while self.gridSize not in [5, 7, 9, 11]:
            try:
                self.gridSize = int(
                    input("Enter a grid Size ( 5 , 7 , 9 or 11): "))
                if self.gridSize not in [5, 7, 9, 11]:
                    print(
                        "Invalid input. Please enter a number equal to : 5 , 7 , 9 or 11.")
            except ValueError:
                print(
                    "Invalid input. Please enter a number equal to : 5 , 7 , 9 or 11. ")
        self.fakeGridSize = self.gridSize
        self.gridSize = self.gridSize*2-1

        # choix du nombre de barrières
        if self.fakeGridSize == 11:
            self.nbBarrierPerPlayer = int(
                input("Enter a barrier number per player (4-40) :"))
            while not (4 <= self.nbBarrierPerPlayer <= 40 and self.nbBarrierPerPlayer % 4 == 0):
                print("Incorrect value . Please try again")
                self.nbBarrierPerPlayer = int(
                    input("Enter a barrier number per player (4-40) :"))

        elif self.fakeGridSize == 9:
            self.nbBarrierPerPlayer = int(
                input("Enter a barrier number per player (4-32) :"))
            while not (4 <= self.nbBarrierPerPlayer <= 32 and self.nbBarrierPerPlayer % 4 == 0):
                print("Incorrect value . Please try again")
                self.nbBarrierPerPlayer = int(
                    input("Enter a barrier number per player (4-32) :"))

        elif self.fakeGridSize == 7:
            self.nbBarrierPerPlayer = int(
                input("Enter a barrier number per player (4-24) :"))
            while not (4 <= self.nbBarrierPerPlayer <= 24 and self.nbBarrierPerPlayer % 4 == 0):
                print("Incorrect value . Please try again")
                self.nbBarrierPerPlayer = int(
                    input("Enter a barrier number per player (4-24) :"))

        elif self.fakeGridSize == 5:
            self.nbBarrierPerPlayer = int(
                input("Enter a barrier number per player (4-12) :"))
            while not (4 <= self.nbBarrierPerPlayer <= 12 and self.nbBarrierPerPlayer % 4 == 0):
                print("Incorrect value . Please try again")
                self.nbBarrierPerPlayer = int(
                    input("Enter a barrier number per player (4-12) :"))

        self.grid = [[case() for i in range(30)] for j in range(30)]

        # cette boucle va attribuer une nature aux cases en fonction
        # de leur position dans le tableau (0 or 1 or 2 or 4 or 5 or 7)

        for i in range(self.gridSize):
            for j in range(self.gridSize):

                if self.nbPlayers == 2:
                    if i == 0 and j == (self.gridSize//2):
                        # initialise le pion du joueur 1 (millieu 1ère ligne)
                        self.grid[i][j].setNature(4)

                    elif (i == self.gridSize-1 and j == self.gridSize//2):
                        # initialise le pion du joueur 2 (millieu 2ème ligne)
                        self.grid[i][j].setNature(5)

                    elif (i % 2 == 0 and j % 2 == 0):
                        # initialise les cases occupables par le pions
                        self.grid[i][j].setNature(0)

                    elif (i % 2 == 1 and j % 2 == 0):
                        # initialise les barrières "-" (en non visisbles)
                        self.grid[i][j].setNature(1)

                    elif (i % 2 == 0 and j % 2 == 1):
                        # initialise les barrières "|" (en non visibles)
                        self.grid[i][j].setNature(2)
                    else:
                        self.grid[i][j].setNature(7)  # barrières "parasites"

                if self.nbPlayers == 3:
                    if i == 0 and j == (self.gridSize//2):
                        # initialise le pions du joueur 1 (millieu 1ère ligne)
                        self.grid[i][j].setNature(4)

                    elif (i == self.gridSize-1 and j == self.gridSize//2):
                        # initialise le pions du joueur 2 (millieu 2ème ligne)
                        self.grid[i][j].setNature(5)

                    elif j == 0 and i == (self.gridSize//2):
                        # initialise le pions du joueur 3 (millieu 1ère colonne)
                        self.grid[i][j].setNature(6)

                    elif (i % 2 == 0 and j % 2 == 0):
                        # initialise les cases occupables par le pions
                        self.grid[i][j].setNature(0)

                    elif (i % 2 == 1 and j % 2 == 0):
                        # initialise les barrières "-" (en non visisbles)
                        self.grid[i][j].setNature(1)

                    elif (i % 2 == 0 and j % 2 == 1):
                        # initialise les barrières "|" (en non visibles)
                        self.grid[i][j].setNature(2)

                    else:
                        self.grid[i][j].setNature(7)  # barrières "parasites"

                if self.nbPlayers == 4:
                    if i == 0 and j == (self.gridSize//2):
                        # initialise le pions du joueur 1 (millieu 1ère ligne)
                        self.grid[i][j].setNature(4)

                    elif (i == self.gridSize-1 and j == self.gridSize//2):
                        # initialise le pions du joueur 2 (millieu 2ème ligne)
                        self.grid[i][j].setNature(5)

                    elif j == 0 and i == (self.gridSize//2):
                        # initialise le pions du joueur 3 (millieu 1ère colonne)
                        self.grid[i][j].setNature(6)

                    elif (j == self.gridSize-1 and i == self.gridSize//2):
                        # initialise le pions du joueur 4 (millieu 2ème colonne)
                        self.grid[i][j].setNature(8)

                    elif (i % 2 == 0 and j % 2 == 0):
                        # initialise les cases occupables par le pions
                        self.grid[i][j].setNature(0)

                    elif (i % 2 == 1 and j % 2 == 0):
                        # initialise les barrières "-" (en non visisbles)
                        self.grid[i][j].setNature(1)

                    elif (i % 2 == 0 and j % 2 == 1):
                        # initialise les barrières "|" (en non visibles)
                        self.grid[i][j].setNature(2)

                    else:
                        self.grid[i][j].setNature(7)  # barrières "parasites

        self.wallSize = 10

        # variables qui servent à améliorer l'affichage graphique
        if self.fakeGridSize == 5:
            self.cellSize = 80
            self.pawnShadow = 4
            self.pawnRadius = self.wallSize//2
            self.settingX = 860
        elif self.fakeGridSize == 7:
            self.cellSize = 60
            self.pawnShadow = 4
            self.pawnRadius = self.wallSize//2
            self.settingX = 880
        elif self.fakeGridSize == 9:
            self.cellSize = 50
            self.pawnShadow = 3
            self.pawnRadius = self.wallSize//2
            self.settingX = 920
        elif self.fakeGridSize == 11:
            self.cellSize = 40
            self.pawnShadow = 3
            self.pawnRadius = 4
            self.settingX = 920

        self.screenSizeX = 1280
        self.screenSizeY = 650
        self.screen = pygame.display.set_mode(
            (self.screenSizeX, self.screenSizeY))
        self.boardSizeX = 630
        self.boardSizeY = 650
        self.board = pygame.Surface((self.boardSizeX, self.boardSizeY))
        self.board.fill(self.Brown)
        self.cell = pygame.Surface((self.cellSize, self.cellSize))
        self.pannelSizeX = self.cellSize*self.fakeGridSize + \
            self.wallSize*(self.fakeGridSize-1)
        self.pannelPositionY = self.cellSize+self.wallSize+self.cellSize * \
            self.fakeGridSize+self.wallSize * \
            (self.fakeGridSize-1)+self.wallSize//2

        # initialisation du nombre de barrières des joueurs
        self.player1barriers = self.nbBarrierPerPlayer
        self.player2barriers = self.nbBarrierPerPlayer
        self.player3barriers = self.nbBarrierPerPlayer
        self.player4Barriers = self.nbBarrierPerPlayer

        self.running = True
        self.player3 = False
        self.player4 = False
        if self.nbPlayers == 3:
            self.player3 = True
        if self.nbPlayers == 4:
            self.player3 = True
            self.player4 = True

        # définition des surfaces de clique pour les in-game menu
        self.exitRect = pygame.Rect(330, 0, self.cellSize, self.cellSize)
        self.settingsRect = pygame.Rect(
            self.settingX, 0, self.cellSize, self.cellSize)
        self.winExitRect = False
        self.rankingRect = False

        self.menuExitRect = None
        self.sfxRect = None
        self.audioRect = None

        # définition de surafaces pour le hover des cellules et murs
        self.cellHover = pygame.Surface(
            (self.cellSize, self.cellSize))
        self.cellHoverBorder = pygame.Surface(
            (self.cellSize, self.wallSize//2))
        self.verticalWallHover = pygame.Surface(
            (self.wallSize, self.cellSize*2+self.wallSize))
        self.horizontalWallHover = pygame.Surface(
            (self.cellSize*2+self.wallSize, self.wallSize))
        # son
        self.audio = False
        self.sfx = False
        self.ShowSettingsMenu = False

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getGrid(self):
        return self.grid

    def setGrid(self, newGrid):
        self.grid = newGrid

    def handlingEvents(self):  # gestion des évènements

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.closeWindow()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if self.exitRect.collidepoint(pos):
                    self.closeWindow()
                if self.settingsRect.collidepoint(pos):
                    if self.ShowSettingsMenu == False:
                        self.ShowSettingsMenu = True
                    else:
                        self.screen.blit(self.board, ((self.screenSizeX - self.boardSizeX) //
                                                      2, (self.screenSizeY - self.boardSizeY) // 2))
                        self.ShowSettingsMenu = False
                        pygame.display.flip()

                if self.ShowSettingsMenu == True:
                    if self.audioRect:
                        if self.audioRect.collidepoint(pos):
                            if self.audio == True:
                                self.audio = False
                            else:
                                self.audio = True
                            if self.ShowSettingsMenu == True:
                                self.screen.blit(self.popupsurface2,
                                                 self.popupsurfaceRect2)
                                self.screen.blit(self.popupsurface,
                                                 self.popupsurfaceRect)
                                pygame.display.flip()

                    if self.sfxRect:
                        if self.sfxRect.collidepoint(pos):
                            if self.sfx == True:
                                self.sfx = False
                            else:
                                self.sfx = True
                            if self.ShowSettingsMenu == True:
                                self.screen.blit(self.popupsurface2,
                                                 self.popupsurfaceRect2)
                                self.screen.blit(self.popupsurface,
                                                 self.popupsurfaceRect)
                                pygame.display.update()

                if self.winExitRect:
                    if self.winExitRect.collidepoint(pos):
                        self.closeWindow()

                # après un click de souris sur le plateau les coordonnées de grille correspondantes sont générées
                x, y = pos
                if self.fakeGridSize == 11:
                    soustraX = 375
                    soustraY = 50
                if self.fakeGridSize == 9:
                    soustraX = 385
                    soustraY = 60
                if self.fakeGridSize == 7:
                    soustraX = 395
                    soustraY = 70
                if self.fakeGridSize == 5:
                    soustraX = 415
                    soustraY = 90

                x -= soustraX
                y -= soustraY

                # clique en dehors du tableau
                while (x < 0 or y < 0 or y == self.fakeGridSize-1):
                    return self.handlingEvents()

                x = self.convertValue(x, self.cellSize)
                y = self.convertValue(y, self.cellSize)

                self.placeWall(x, y)
                self.movePawn(x, y)
        return

    def movePawn(self, x, y):
        if self.ShowSettingsMenu == False:
            # fonction déplacement des pions
            for i in range(self.gridSize):
                for j in range(self.gridSize):
                    if 0 <= x < self.gridSize+2 and 0 <= y < self.gridSize+2:

                        if self.currentPlayer == 1:
                            # déplacments normaux (gauche , droite , haut , bat)
                            if self.grid[y][x-2].getNature() == 4 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 4 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 4 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 4 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière )
                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.nextPlayer()
                                return

                        if self.currentPlayer == 2:
                            # déplacments normaux (gauche , droite , haut , bat)
                            # verticale
                            if self.grid[y][x-2].getNature() == 5 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 5 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 5 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 5 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière  )
                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.nextPlayer()
                                return

                        if self.currentPlayer == 3:
                            # déplacments normaux (gauche , droite , haut , bat)
                            if self.grid[y][x-2].getNature() == 6 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 6 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 6 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 6 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière  )
                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.nextPlayer()
                                return

                        if self.currentPlayer == 4:
                            # déplacments normaux (gauche , droite , haut , bat)
                            if self.grid[y][x-2].getNature() == 8 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 8 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 8 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 8 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière  )
                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return
                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.nextPlayer()
                                return

    def placeWall(self, x, y):
        if self.ShowSettingsMenu == False:
            # clique à la limite droite du tableau
            while (x == self.gridSize-1):
                return self.handlingEvents()

            gridCopy = copy.deepcopy(self.grid)
            # fonction placement de murs
            if (self.currentPlayer == 1 and self.player1barriers > 0) or (self.currentPlayer == 2 and self.player2barriers > 0) or (self.currentPlayer == 3 and self.player3barriers > 0) or (self.currentPlayer == 4 and self.player4Barriers > 0):

                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if 0 <= x+2 < self.gridSize+2 and 0 <= y+2 < self.gridSize+2:
                            if self.grid[x][y].getNature() == 1 and self.grid[y][x].getNature() != 10 and self.grid[y][x].getNature() != 20 and self.grid[y+1][x].getNature() != 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x].getNature() != 10 and self.grid[y+2][x].getNature() != 20:

                                self.grid[y][x].setNature(10)
                                self.grid[y+1][x].setNature(10)
                                self.grid[y+2][x].setNature(10)
                                if self.verifyPath(gridCopy) is True:
                                    self.horizontalWallDrawing(x, y)
                                    if self.currentPlayer == 1:
                                        self.player1barriers -= 1
                                    elif self.currentPlayer == 2:
                                        self.player2barriers -= 1
                                    elif self.currentPlayer == 3:
                                        self.player3barriers -= 1
                                    elif self.currentPlayer == 4:
                                        self.player4Barriers -= 1
                                    self.nextPlayer()
                                    return

                            elif self.grid[x][y].getNature() == 2 and self.grid[y][x].getNature() != 20 and self.grid[y][x].getNature() != 10 and self.grid[y][x+1].getNature() != 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y][x+2].getNature() != 20 and self.grid[y][x+2].getNature() != 10:
                                self.grid[y][x].setNature(20)
                                self.grid[y][x+1].setNature(20)
                                self.grid[y][x+2].setNature(20)
                                if self.verifyPath(gridCopy) is True:
                                    self.verticalWallDrawing(x, y)
                                    if self.currentPlayer == 1:
                                        self.player1barriers -= 1
                                    elif self.currentPlayer == 2:
                                        self.player2barriers -= 1
                                    elif self.currentPlayer == 3:
                                        self.player3barriers -= 1
                                    elif self.currentPlayer == 4:
                                        self.player4Barriers -= 1
                                    self.nextPlayer()
                                    return

    def verifyPath(self, gridCopy):
        # vérification des chemins
        if self.nbPlayers == 2:
            if self.pathFinding(4, self.grid) is False or self.pathFinding(5, self.grid) is False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = copy.deepcopy(gridCopy)
                print("impossible to place this wall . Please try again")
            else:
                return True

        elif self.nbPlayers == 3:
            if self.pathFinding(4, self.grid) is False or self.pathFinding(5, self.grid) is False or self.pathFinding(6, self.grid) is False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = copy.deepcopy(gridCopy)
                print("impossible to place this wall . Please try again")
            else:
                return True

        elif self.nbPlayers == 4:
            if self.pathFinding(4, self.grid) is False or self.pathFinding(5, self.grid) is False or self.pathFinding(6, self.grid) is False or self.pathFinding(8, self.grid) is False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = copy.deepcopy(gridCopy)
                print("impossible to place this wall . Please try again")
            else:
                return True

    def displayHover(self):
        if self.ShowSettingsMenu == False:
            for line in range(self.gridSize):
                for col in range(self.gridSize):
                    # hover mur horizontaux
                    if self.grid[col][line].getNature() == 1 and self.grid[col][line+1].getNature() == 7 and self.grid[col][line+2].getNature() == 1:
                        x = self.indexToPixels(line // 2)
                        y = self.indexToPixels(col // 2)
                        self.wallRect = pygame.Rect(
                            x + ((self.screenSizeX - self.boardSizeX) // 2), y+self.cellSize, self.cellSize, self.wallSize)
                        self.horizontalWallHoverCopy = self.horizontalWallHover.copy()
                        pos = pygame.mouse.get_pos()

                        if self.wallRect.collidepoint(pos):
                            self.horizontalWallHoverCopy.fill(self.black)
                        else:
                            self.horizontalWallHoverCopy.set_colorkey(
                                self.horizontalWallHoverCopy.get_at((0, 0)))

                        self.screen.blit(self.horizontalWallHoverCopy, (x + ((self.screenSizeX - self.boardSizeX) //
                                                                             2), y+self.cellSize))

                    # hover mur verticaux
                    if self.grid[col][line].getNature() == 2 and self.grid[col+1][line].getNature() == 7 and self.grid[col+2][line].getNature() == 2:
                        x = self.indexToPixels(line // 2)
                        y = self.indexToPixels(col // 2)
                        self.wallRect = pygame.Rect(
                            x + ((self.screenSizeX - self.boardSizeX) // 2)+self.cellSize, y, self.wallSize, self.cellSize)
                        self.verticalWallHoverCopy = self.verticalWallHover.copy()
                        pos = pygame.mouse.get_pos()

                        if self.wallRect.collidepoint(pos):
                            self.verticalWallHoverCopy.fill(self.black)
                        else:
                            self.verticalWallHoverCopy.set_colorkey(
                                self.verticalWallHoverCopy.get_at((0, 0)))
                            # self.verticalWallHoverCopy.fill(self.green)

                        self.screen.blit(self.verticalWallHoverCopy, (x + ((self.screenSizeX - self.boardSizeX) //
                                                                           2)+self.cellSize, y))

                    # hover des cellules du board
                    if self.grid[col][line].getNature() == 0:
                        x = self.indexToPixels(line // 2)
                        y = self.indexToPixels(col // 2)
                        self.cellRect = pygame.Rect(
                            x + ((self.screenSizeX - self.boardSizeX) // 2), y, self.cellSize, self.cellSize)
                        self.cellHoverCopy = self.cellHover.copy()
                        self.cellHoverBorderCopy = self.cellHoverBorder.copy()
                        pos = pygame.mouse.get_pos()

                        if self.cellRect.collidepoint(pos):
                            self.cellHoverCopy.fill(self.Red)
                            self.cellHoverBorderCopy.fill(self.darkRed)
                        else:
                            self.cellHoverCopy.set_colorkey(
                                self.cellHoverCopy.get_at((0, 0)))

                            self.cellHoverBorderCopy.set_colorkey(
                                self.cellHoverBorderCopy.get_at((0, 0)))

                        self.screen.blit(self.cellHoverCopy, (x + ((self.screenSizeX - self.boardSizeX) //
                                                                   2), y))
                        self.screen.blit(self.cellHoverBorderCopy, (x + ((self.screenSizeX - self.boardSizeX) //
                                                                         2), y+self.cellSize))

    def displayScreen(self):  # affichage de l'écran pygame et de la  grille de jeu
        self.screen.fill(self.beige6)
        for line in range(self.gridSize):
            for col in range(self.gridSize):
                if line % 2 == 0 and col % 2 == 0:
                    x = self.indexToPixels(line // 2)
                    y = self.indexToPixels(col // 2)
                    self.cell.fill(self.beige)
                    self.board.blit(self.cell, (x, y))

                if self.grid[col][line].getNature() == 4:

                    x = self.indexToPixels(line // 2)
                    y = self.indexToPixels(col // 2)
                    self.vari = (x, y)
                    cell1 = pygame.Surface((self.cellSize, self.cellSize))
                    cell1.fill(self.beige)

                    circle1 = self.drawCircle(
                        cell1, self.cellSize//2, self.cellSize//2, (self.cellSize//2)-self.pawnRadius, self.darkBlue)

                    circle10 = self.drawCircle(
                        cell1, self.cellSize//2, (self.cellSize//2)-self.pawnShadow, (self.cellSize//2)-self.pawnRadius, self.blue)

                    self.board.blit(cell1, (x, y))

                if self.grid[col][line].getNature() == 5:

                    x = self.indexToPixels(line // 2)
                    y = self.indexToPixels(col // 2)
                    cell2 = pygame.Surface((self.cellSize, self.cellSize))
                    cell2.fill(self.beige)
                    circle2 = self.drawCircle(
                        cell2, self.cellSize//2, self.cellSize//2, (self.cellSize//2)-self.pawnRadius, self.darkPink)
                    circle20 = self.drawCircle(
                        cell2, self.cellSize//2, (self.cellSize//2)-self.pawnShadow, (self.cellSize//2)-self.pawnRadius, self.pink)
                    self.board.blit(cell2, (x, y))

                if self.grid[col][line].getNature() == 6:

                    x = self.indexToPixels(line // 2)
                    y = self.indexToPixels(col // 2)
                    cell3 = pygame.Surface((self.cellSize, self.cellSize))
                    cell3.fill(self.beige)
                    circle3 = self.drawCircle(
                        cell3, self.cellSize//2, self.cellSize//2, self.cellSize//2-self.pawnRadius, self.darkYellow)
                    self.board.blit(cell3, (x, y))

                    circle30 = self.drawCircle(
                        cell3, self.cellSize//2, (self.cellSize//2)-self.pawnShadow, (self.cellSize//2)-self.pawnRadius, self.yellow)

                    self.board.blit(cell3, (x, y))

                if self.grid[col][line].getNature() == 8:

                    x = self.indexToPixels(line // 2)
                    y = self.indexToPixels(col // 2)
                    cell4 = pygame.Surface((self.cellSize, self.cellSize))
                    cell4.fill(self.beige)
                    circle4 = self.drawCircle(
                        cell4, self.cellSize//2, self.cellSize//2, self.cellSize//2-self.pawnRadius, self.darkOrange)
                    self.board.blit(cell4, (x, y))

                    circle40 = self.drawCircle(
                        cell4, self.cellSize//2, (self.cellSize//2)-self.pawnShadow, (self.cellSize//2)-self.pawnRadius, self.orange)

                    self.board.blit(cell4, (x, y))
        self.displayScore()
        self.displayButton()
        self.screen.blit(self.board, ((self.screenSizeX - self.boardSizeX) //
                         2, (self.screenSizeY - self.boardSizeY) // 2))

    def displayScore(self):
        # informations pannel 1:
        self.pannel1 = pygame.Surface((self.pannelSizeX, self.cellSize))
        self.pannel1.fill(self.black)
        # border
        self.border = pygame.Surface((self.pannelSizeX, self.wallSize//2))
        self.border.fill(self.black2)
        # informations pannel 2
        self.pannel2 = pygame.Surface((self.pannelSizeX, self.cellSize))
        self.pannel2.fill(self.black)
        # contenu pannel
        # Charger la police de caractères
        self.font = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        # Charger la police de caractère
        self.fontTitle = pygame.font.Font(
            "assets/font/chalk_scratch.otf", 30)
        self.textSurfaceTitle = self.fontTitle.render(
            'QUORIDOR', True, self.whitheSmoke2)  # Créer la surface de texte
        self.textSurface1 = self.font.render(
            'Player 1 Walls : '+str(self.player1barriers), True, self.whitheSmoke2)
        self.textSurface2 = self.font.render(
            'Player 2 Walls : '+str(self.player2barriers), True, self.whitheSmoke2)
        if self.player3:
            self.textSurface3 = self.font.render(
                'Player 3 Walls :'+str(self.player3barriers), True, self.whitheSmoke2)
        if self.player4:
            self.textSurface4 = self.font.render(
                'Player 4 Walls :'+str(self.player4Barriers), True, self.whitheSmoke2)
        # positionnement  pannels contenu
        if self.fakeGridSize == 5:
            scoreRecPositionX = 370
        elif self.fakeGridSize == 7:
            scoreRecPositionX = 410
        elif self.fakeGridSize == 9:
            scoreRecPositionX = 460
        elif self.fakeGridSize == 11:
            scoreRecPositionX = 470

        # Récupérer le rectangle de la surface de texte
        self.textRectTitle = self.textSurfaceTitle.get_rect()
        # Définir la position du texte
        self.textRectTitle.center = (
            self.pannelSizeX//2, self.cellSize//2)

        # Récupérer le rectangle de la surface de texte
        self.textRect1 = self.textSurface1.get_rect()
        # Définir la position du texte
        self.textRect1.center = (71, self.cellSize//4)

        # Récupérer le rectangle de la surface de texte
        self.textRect2 = self.textSurface2.get_rect()
        # Définir la position du texte
        self.textRect2.center = (71, (self.cellSize//4)*3)

        if self.player3:
            # Récupérer le rectangle de la surface de texte
            self.textRect3 = self.textSurface3.get_rect()
            # Définir la position du texte
            self.textRect3.center = (scoreRecPositionX, self.cellSize//4)
        if self.player4:
            # Récupérer le rectangle de la surface de texte
            self.textRect4 = self.textSurface4.get_rect()
            # Définir la position du texte
            self.textRect4.center = (
                scoreRecPositionX, (self.cellSize//4)*3)

        # affichage sur l'écran pygame
        self.pannel1.fill(self.black)
        self.pannel2.fill(self.black)
        self.pannel1.blit(self.textSurfaceTitle, self.textRectTitle)
        self.pannel2.blit(self.textSurface1, self.textRect1)
        self.pannel2.blit(self.textSurface2, self.textRect2)
        if self.player3:
            self.pannel2.blit(self.textSurface3, self.textRect3)
        if self.player4:
            self.pannel2.blit(self.textSurface4, self.textRect4)
        self.board.blit(
            self.border, ((self.cellSize+self.wallSize, self.cellSize)))
        self.board.blit(self.pannel1, ((self.cellSize+self.wallSize, 0)))
        self.board.blit(
            self.pannel2, ((self.cellSize+self.wallSize, self.pannelPositionY)))
        self.board.blit(self.border, (self.cellSize +
                        self.wallSize, self.pannelPositionY+self.cellSize))

    def displayButton(self):
        rankingImage = pygame.image.load("assets/images/ranking.png")
        rankingImage = pygame.transform.scale(
            rankingImage, (self.cellSize, self.cellSize))

        settingImage = pygame.image.load("assets/images/settings3.png")
        settingImage = pygame.transform.scale(
            settingImage, (self.cellSize//2, self.cellSize//2))
        settingImage_rect = settingImage.get_rect()
        settingImage_rect.center = (self.cellSize//2, self.cellSize//2)

        # Charger la police de caractères
        fontButton = pygame.font.Font("assets/font/chalk_scratch.otf", 25)
        exitMessage = fontButton.render('Exit', True, self.whitheSmoke2)
        exitMessage_rect = exitMessage.get_rect()
        exitMessage_rect.center = (self.cellSize//2, self.cellSize//2)

        exitButton = pygame.Surface((self.cellSize, self.cellSize))
        exitButton.fill(self.Red)
        exitButton_border = pygame.Surface(
            (self.cellSize, self.wallSize//2))
        exitButton_border.fill(self.darkRed)

        rankingButton = pygame.Surface((self.cellSize, self.cellSize))
        rankingButton.fill(self.black)
        rankingButton_border = pygame.Surface(
            (self.cellSize, self.wallSize//2))
        rankingButton_border.fill(self.black2)

        settingButton = pygame.Surface((self.cellSize, self.cellSize))
        settingButton.fill(self.black)
        settingButtonBorder = pygame.Surface(
            (self.cellSize, self.wallSize//2))
        settingButtonBorder.fill(self.black2)

        # création du bloc annonçant le joueur qui doit jouer
        if self.currentPlayer == 1:
            actualPlayerColor = self.blue
            actualPlayerBorder = self.darkBlue
        if self.currentPlayer == 2:
            actualPlayerColor = self.pink
            actualPlayerBorder = self.darkPink
        if self.currentPlayer == 3:
            actualPlayerColor = self.yellow
            actualPlayerBorder = self.darkYellow
        if self.currentPlayer == 4:
            actualPlayerColor = self.orange
            actualPlayerBorder = self.darkOrange

        actualPlayerButton = pygame.Surface((self.cellSize, self.cellSize))
        actualPlayerButton.fill(actualPlayerColor)
        actualPlayerButton_border = pygame.Surface(
            (self.cellSize, self.wallSize//2))
        actualPlayerButton_border.fill(actualPlayerBorder)

        if self.fakeGridSize == 9:
            sideStickX = self.wallSize*2
        if self.fakeGridSize == 11:
            sideStickX = self.wallSize
        if self.fakeGridSize == 9 or self.fakeGridSize == 11:
            sideStick = pygame.Surface((sideStickX, self.boardSizeY))
        if self.fakeGridSize == 9 or self.fakeGridSize == 11:
            sideStick.fill(self.Brown)

        rankingButton.blit(rankingImage, (0, 0))
        settingButton.blit(settingImage, settingImage_rect)
        self.board.blit(actualPlayerButton, (self.cellSize+self.wallSize +
                        self.wallSize//2+self.pannelSizeX, self.pannelPositionY))
        self.board.blit(actualPlayerButton_border, (self.cellSize+self.wallSize +
                        self.wallSize//2+self.pannelSizeX, self.pannelPositionY+self.cellSize))
        self.board.blit(settingButton, (self.cellSize +
                        self.wallSize+self.wallSize//2+self.pannelSizeX, 0))
        self.board.blit(settingButtonBorder, (self.cellSize+self.wallSize +
                        self.wallSize//2+self.pannelSizeX, self.cellSize))

        exitButton.blit(exitMessage, exitMessage_rect)
        self.board.blit(rankingButton, (self.wallSize //
                        2, self.pannelPositionY))
        self.board.blit(rankingButton_border, (self.wallSize //
                        2, self.pannelPositionY+self.cellSize))
        self.board.blit(exitButton, ((self.wallSize//2, 0)))
        self.board.blit(exitButton_border,
                        ((self.wallSize//2, self.cellSize)))

        if self.fakeGridSize == 9 or self.fakeGridSize == 11:
            self.screen.blit(sideStick, (((self.screenSizeX - self.boardSizeX) // 2) +
                             self.boardSizeX, (self.screenSizeY - self.boardSizeY) // 2))

    def indexToPixels(self, index):
        # converti un index de grille en index de plateau
        return (index + 1) * self.wallSize + (index + 1) * self.cellSize

    def drawCircle(self, surface, x, y, radius, color):
        gfxdraw.aacircle(surface, x, y, radius, color)
        gfxdraw.filled_circle(surface, x, y, radius, color)

    def horizontalWallDrawing(self, x, y):
        j = self.indexToPixels(x//2)+self.cellSize
        i = self.indexToPixels(y//2)
        pygame.draw.rect(self.board, self.black, (j, i, self.wallSize,
                                                  2*self.cellSize+self.wallSize+self.wallSize//2))

    def verticalWallDrawing(self, x, y):
        j = self.indexToPixels(x//2)
        i = self.indexToPixels(y//2)+self.cellSize
        pygame.draw.rect(self.board, self.black, (j, i, 2 *
                                                  self.cellSize+self.wallSize, self.wallSize))

    def convertValue(self, value, n):
        intervals = [
            (0, n),
            (n, (n+10)),
            ((n+10), (n+10+n)),
            ((n+10+n), (n+10+n+10)),
            ((n+10+n+10), (n+10+n+10+n)),
            ((n+10+n+10+n), (n+10+n+10+n+10)),
            ((n+10+n+10+n+10), (n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n), (n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10), (n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n), (n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10), (n+10+n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n+10+n), (n+10+n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10+n+10), (n+10+n+10+n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10)),
            ((n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10),
             (n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n+10+n))
        ]
        for i, interval in enumerate(intervals):
            if value >= interval[0] and value < interval[1]:
                return i
            if i == 22:
                break
        return self.handlingEvents()

    def nextPlayer(self):
        if self.nbPlayers > self.currentPlayer:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 1

    def checkWin(self):
        win = False
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if (self.grid[i][j].getNature() == 4 and i == self.gridSize-1) or (self.grid[i][j].getNature() == 5 and i == 0) or (self.grid[i][j].getNature() == 8 and j == 0) or (self.grid[i][j].getNature() == 6 and j == self.gridSize-1):
                    win = True
                    break
        return win
        # après un mouvement current_player = current_player + 1 , donc le gagant est currentPlayer- 1

    def displayWinner(self):
        if self.currentPlayer-1 == 0 and self.nbPlayers == 2:
            print(colored("Player " + str(self.nbPlayers) + " wins!", "green"))
        elif self.currentPlayer-1 == 0 and self.nbPlayers == 3:
            print(colored("Player " + str(self.nbPlayers) + " wins!", "yellow"))
        elif self.currentPlayer-1 == 0 and self.nbPlayers == 4:
            print(colored("Player " + str(self.nbPlayers) + " wins!", "magenta"))

        elif self.currentPlayer-1 == 1:
            print(colored("Player 1 wins !", "blue"))
        elif self.currentPlayer-1 == 2:
            print(colored("Player 2 wins !", "green"))
        elif self.currentPlayer-1 == 3:
            print(colored("Player 3 wins !", "yellow"))

    def displayGrid(self):  # affiche un tableau d'objet case
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                # Recupere la nature des cases puis les affiches en fonction
                print(self.grid[i][j].checkNature(), end=" ")
            print()

    def drawCellHeight(self):  # amélioration de l'affichage des cellules
        for line in range(self.gridSize):
            for col in range(self.gridSize):
                if col > 1:

                    x = self.indexToPixels(line // 2)
                    y = self.indexToPixels(col // 2) - self.wallSize
                    width = self.cellSize
                    height = self.wallSize//2
                    pygame.draw.rect(
                        self.board, self.lightBrown, (x, y, width, height))

    def drawPlayerDirection(self):  # affichage des directions
        if self.ShowSettingsMenu == False:

            if not self.checkWin():
                if self.currentPlayer == 1:
                    for line in range(self.gridSize):
                        for col in range(self.gridSize):
                            hover = False
                            # direction normales (droite , gauche , haut , bas)
                            if col-2 < self.gridSize:
                                if self.grid[col-2][line].getNature() == 4 and self.grid[col-1][line].getNature() != 20 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            if col+2 < self.gridSize:
                                if self.grid[col+2][line].getNature() == 4 and self.grid[col+1][line].getNature() != 20 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            if line+2 < self.gridSize:
                                if self.grid[col][line+2].getNature() == 4 and self.grid[col][line+1].getNature() != 10 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            if line-2 < self.gridSize:
                                if self.grid[col][line-2].getNature() == 4 and self.grid[col][line-1].getNature() != 10 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            # direction saut de pion adverse
                            if col-4 < self.gridSize and col-2 < self.gridSize:
                                if self.grid[col-4][line].getNature() == 4 and (self.grid[col-2][line].getNature() == 5 or self.grid[col-2][line].getNature() == 6 or self.grid[col-2][line].getNature() == 8) and self.grid[col-1][line].getNature() != 20 and self.grid[col-3][line].getNature() != 20 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            if col+4 < self.gridSize and col+2 < self.gridSize:
                                if self.grid[col+4][line].getNature() == 4 and (self.grid[col+2][line].getNature() == 5 or self.grid[col+2][line].getNature() == 6 or self.grid[col+2][line].getNature() == 8) and self.grid[col+1][line].getNature() != 20 and self.grid[col+3][line].getNature() != 20 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            if line-4 < self.gridSize and line-2 < self.gridSize:
                                if self.grid[col][line-4].getNature() == 4 and (self.grid[col][line-2].getNature() == 5 or self.grid[col][line-2].getNature() == 6 or self.grid[col][line-2].getNature() == 8) and self.grid[col][line-1].getNature() != 10 and self.grid[col][line-3].getNature() != 10 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            if line+4 < self.gridSize and line+2 < self.gridSize:
                                if self.grid[col][line+4].getNature() == 4 and (self.grid[col][line+2].getNature() == 5 or self.grid[col][line+2].getNature() == 6 or self.grid[col][line+2].getNature() == 8) and self.grid[col][line+1].getNature() != 10 and self.grid[col][line+3].getNature() != 10 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                    hover = True
                                    x = self.indexToPixels(line // 2)
                                    y = self.indexToPixels(col // 2)
                                    self.cell.fill(self.beige3)
                                    self.board.blit(self.cell, (x, y))

                            # directions déplacement en diagonale ( pion adverse + barrière )
                            if self.grid[col][line].getNature() == 0 and self.grid[col-1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() == 4 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col+1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() == 4 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col+1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() == 4 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col-1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() == 4 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col+2][line-1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() == 4 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col+2][line+1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() == 4 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col-2][line+1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() == 4 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col][line].getNature() == 0 and self.grid[col-2][line-1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() == 4 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[col+2][line+2].getNature() == 4 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col+2][line-2].getNature() == 4 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col-2][line+2].getNature() == 4 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col-2][line-2].getNature() == 4 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            # Horizontale
                            if self.grid[col-2][line-2].getNature() == 4 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col-2][line+2].getNature() == 4 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col+2][line-2].getNature() == 4 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                            if self.grid[col+2][line+2].getNature() == 4 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                                hover = True
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

            if self.currentPlayer == 2:
                for line in range(self.gridSize):
                    for col in range(self.gridSize):
                        # direction normales (droite , gauche , haut , bas)
                        if col-2 < self.gridSize:
                            if self.grid[col-2][line].getNature() == 5 and self.grid[col-1][line].getNature() != 20 and (self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if col+2 < self.gridSize:
                            if self.grid[col+2][line].getNature() == 5 and self.grid[col+1][line].getNature() != 20 and (self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line+2 < self.gridSize:
                            if self.grid[col][line+2].getNature() == 5 and self.grid[col][line+1].getNature() != 10 and (self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))
                        if line-2 < self.gridSize:
                            if self.grid[col][line-2].getNature() == 5 and self.grid[col][line-1].getNature() != 10 and (self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        # direction saut de pion adverse
                        if col-4 < self.gridSize and col-2 < self.gridSize:
                            if self.grid[col-4][line].getNature() == 5 and (self.grid[col-2][line].getNature() == 4 or self.grid[col-2][line].getNature() == 6 or self.grid[col-2][line].getNature() == 8) and self.grid[col-1][line].getNature() != 20 and self.grid[col-3][line].getNature() != 20 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if col+4 < self.gridSize and col+2 < self.gridSize:
                            if self.grid[col+4][line].getNature() == 5 and (self.grid[col+2][line].getNature() == 4 or self.grid[col+2][line].getNature() == 6 or self.grid[col+2][line].getNature() == 8) and self.grid[col+1][line].getNature() != 20 and self.grid[col+3][line].getNature() != 20 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line-4 < self.gridSize and line-2 < self.gridSize:
                            if self.grid[col][line-4].getNature() == 5 and (self.grid[col][line-2].getNature() == 4 or self.grid[col][line-2].getNature() == 6 or self.grid[col][line-2].getNature() == 8) and self.grid[col][line-1].getNature() != 10 and self.grid[col][line-3].getNature() != 10 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line+4 < self.gridSize and line+2 < self.gridSize:
                            if self.grid[col][line+4].getNature() == 5 and (self.grid[col][line+2].getNature() == 4 or self.grid[col][line+2].getNature() == 6 or self.grid[col][line+2].getNature() == 8) and self.grid[col][line+1].getNature() != 10 and self.grid[col][line+3].getNature() != 10 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        # directions déplacement en diagonale ( pion adverse + barrière )
                        if self.grid[col][line].getNature() == 0 and self.grid[col-1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() == 5 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() == 5 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() == 5 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() == 5 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+2][line-1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() == 5 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+2][line+1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() == 5 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-2][line+1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() == 5 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-2][line-1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() == 5 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        # déplacement en diagonale ( pion adverse + pion adverse )
                        # verticale
                        if self.grid[col+2][line+2].getNature() == 5 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line-2].getNature() == 5 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line+2].getNature() == 5 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line-2].getNature() == 5 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        # Horizontale
                        if self.grid[col-2][line-2].getNature() == 5 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line+2].getNature() == 5 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line-2].getNature() == 5 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line+2].getNature() == 5 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

            if self.currentPlayer == 3:
                for line in range(self.gridSize):
                    for col in range(self.gridSize):
                        # direction normales (droite , gauche , haut , bas)
                        if col-2 < self.gridSize:
                            if self.grid[col-2][line].getNature() == 6 and self.grid[col-1][line].getNature() != 20 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if col+2 < self.gridSize:
                            if self.grid[col+2][line].getNature() == 6 and self.grid[col+1][line].getNature() != 20 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line+2 < self.gridSize:
                            if self.grid[col][line+2].getNature() == 6 and self.grid[col][line+1].getNature() != 10 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))
                        if line-2 < self.gridSize:
                            if self.grid[col][line-2].getNature() == 6 and self.grid[col][line-1].getNature() != 10 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        # direction saut de pion adverse
                        if col-4 < self.gridSize and col-2 < self.gridSize:
                            if self.grid[col-4][line].getNature() == 6 and (self.grid[col-2][line].getNature() == 5 or self.grid[col-2][line].getNature() == 4 or self.grid[col-2][line].getNature() == 8) and self.grid[col-1][line].getNature() != 20 and self.grid[col-3][line].getNature() != 20 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if col+4 < self.gridSize and col+2 < self.gridSize:
                            if self.grid[col+4][line].getNature() == 6 and (self.grid[col+2][line].getNature() == 5 or self.grid[col+2][line].getNature() == 4 or self.grid[col+2][line].getNature() == 8) and self.grid[col+1][line].getNature() != 20 and self.grid[col+3][line].getNature() != 20 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line-4 < self.gridSize and line-2 < self.gridSize:
                            if self.grid[col][line-4].getNature() == 6 and (self.grid[col][line-2].getNature() == 5 or self.grid[col][line-2].getNature() == 4 or self.grid[col][line-2].getNature() == 8) and self.grid[col][line-1].getNature() != 10 and self.grid[col][line-3].getNature() != 10 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line+4 < self.gridSize and line+2 < self.gridSize:
                            if self.grid[col][line+4].getNature() == 6 and (self.grid[col][line+2].getNature() == 5 or self.grid[col][line+2].getNature() == 4 or self.grid[col][line+2].getNature() == 8) and self.grid[col][line+1].getNature() != 10 and self.grid[col][line+3].getNature() != 10 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 4 and self.grid[col][line].getNature() != 8:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        # directions déplacement en diagonale ( pion adverse + barrière )
                        if self.grid[col][line].getNature() == 0 and self.grid[col-1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() == 6 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() == 6 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))
                        if self.grid[col][line].getNature() == 0 and self.grid[col+1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() == 6 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() == 6 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+2][line-1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() == 6 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+2][line+1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() == 6 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-2][line+1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() == 6 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-2][line-1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() == 6 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        # déplacement en diagonale ( pion adverse + pion adverse )
                        # verticale
                        if self.grid[col+2][line+2].getNature() == 6 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line-2].getNature() == 6 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line+2].getNature() == 6 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line-2].getNature() == 6 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        # Horizontale
                        if self.grid[col-2][line-2].getNature() == 6 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line+2].getNature() == 6 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line-2].getNature() == 6 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line+2].getNature() == 6 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

            if self.currentPlayer == 4:
                for line in range(self.gridSize):
                    for col in range(self.gridSize):
                        # direction normales (droite , gauche , haut , bas)

                        if col-2 < self.gridSize:
                            if self.grid[col-2][line].getNature() == 8 and self.grid[col-1][line].getNature() != 20 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if col+2 < self.gridSize:
                            if self.grid[col+2][line].getNature() == 8 and self.grid[col+1][line].getNature() != 20 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line+2 < self.gridSize:
                            if self.grid[col][line+2].getNature() == 8 and self.grid[col][line+1].getNature() != 10 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))
                        if line-2 < self.gridSize:
                            if self.grid[col][line-2].getNature() == 8 and self.grid[col][line-1].getNature() != 10 and (self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4):
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        # direction saut de pion adverse
                        if col-4 < self.gridSize and col-2 < self.gridSize:
                            if self.grid[col-4][line].getNature() == 8 and (self.grid[col-2][line].getNature() == 5 or self.grid[col-2][line].getNature() == 6 or self.grid[col-2][line].getNature() == 4) and self.grid[col-1][line].getNature() != 20 and self.grid[col-3][line].getNature() != 20 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if col+4 < self.gridSize and col+2 < self.gridSize:
                            if self.grid[col+4][line].getNature() == 8 and (self.grid[col+2][line].getNature() == 5 or self.grid[col+2][line].getNature() == 6 or self.grid[col+2][line].getNature() == 4) and self.grid[col+1][line].getNature() != 20 and self.grid[col+3][line].getNature() != 20 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line-4 < self.gridSize and line-2 < self.gridSize:
                            if self.grid[col][line-4].getNature() == 8 and (self.grid[col][line-2].getNature() == 5 or self.grid[col][line-2].getNature() == 6 or self.grid[col][line-2].getNature() == 4) and self.grid[col][line-1].getNature() != 10 and self.grid[col][line-3].getNature() != 10 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        if line+4 < self.gridSize and line+2 < self.gridSize:
                            if self.grid[col][line+4].getNature() == 8 and (self.grid[col][line+2].getNature() == 5 or self.grid[col][line+2].getNature() == 6 or self.grid[col][line+2].getNature() == 4) and self.grid[col][line+1].getNature() != 10 and self.grid[col][line+3].getNature() != 10 and self.grid[col][line].getNature() != 5 and self.grid[col][line].getNature() != 6 and self.grid[col][line].getNature() != 4:
                                x = self.indexToPixels(line // 2)
                                y = self.indexToPixels(col // 2)
                                self.cell.fill(self.beige3)
                                self.board.blit(self.cell, (x, y))

                        # directions déplacement en diagonale ( pion adverse + barrière )
                        if self.grid[col][line].getNature() == 0 and self.grid[col-1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() == 8 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() == 8 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))
                        if self.grid[col][line].getNature() == 0 and self.grid[col+1][line+2].getNature() == 20 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() == 8 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line+1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-1][line-2].getNature() == 20 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() == 8 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col][line-1].getNature() != 10:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))
                        if self.grid[col][line].getNature() == 0 and self.grid[col+2][line-1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() == 8 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col+2][line+1].getNature() == 10 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() == 8 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-2][line+1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() == 8 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col][line].getNature() == 0 and self.grid[col-2][line-1].getNature() == 10 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() == 8 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col-1][line].getNature() != 20:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        # déplacement en diagonale ( pion adverse + pion adverse )
                        # verticale
                        if self.grid[col+2][line+2].getNature() == 8 and self.grid[col][line+2].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line-2].getNature() == 8 and self.grid[col][line-2].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line+2].getNature() == 8 and self.grid[col][line+2].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col][line+1].getNature() != 10 and self.grid[col-1][line+2].getNature() != 20 and self.grid[col+1][line+2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line-2].getNature() == 8 and self.grid[col][line-2].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col][line-1].getNature() != 10 and self.grid[col+1][line-2].getNature() != 20 and self.grid[col-1][line-2].getNature() != 20 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        # Horizontale
                        if self.grid[col-2][line-2].getNature() == 8 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line+2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col-2][line+2].getNature() == 8 and self.grid[col-2][line].getNature() != 0 and self.grid[col-2][line-2].getNature() != 0 and self.grid[col-1][line].getNature() != 20 and self.grid[col-2][line-1].getNature() != 10 and self.grid[col-2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line-2].getNature() == 8 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line+2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

                        if self.grid[col+2][line+2].getNature() == 8 and self.grid[col+2][line].getNature() != 0 and self.grid[col+2][line-2].getNature() != 0 and self.grid[col+1][line].getNature() != 20 and self.grid[col+2][line-1].getNature() != 10 and self.grid[col+2][line+1].getNature() != 10 and self.grid[col][line].getNature() == 0:
                            x = self.indexToPixels(line // 2)
                            y = self.indexToPixels(col // 2)
                            self.cell.fill(self.beige3)
                            self.board.blit(self.cell, (x, y))

            self.screen.blit(self.board, ((self.screenSizeX - self.boardSizeX) //
                                          2, (self.screenSizeY - self.boardSizeY) // 2))

    def pathFinding(self, start, grid):

        # recherche du joueur sur la grille (start = référence du joueur)
        startCoord = None  # ajout d'une valeur par défaut pour startCoord
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if grid[i][j].getNature() == start:
                    x = i
                    y = j
                    # recuperation des coordonnées du joueur
                    startCoord = (x, y)
                    break

            if startCoord != None:
                queue = []
                queue.append(startCoord)
                visited = set()
                visited.add(startCoord)

        # tant que des voisins n'ont pas encore été checkés et qu'aucun chemin n'a été trouvé
        while len(queue) > 0:
            curr_node = queue.pop(0)
            row, col = curr_node

            if start == 4:
                if row == self.gridSize-1:
                    return True  # chemin trouvé pour joueur 1
            elif start == 5:
                if row == 0:
                    return True  # chemin trouvé pour joueur 2
            elif start == 6:
                if col == self.gridSize-1:
                    return True  # chemin trouvé pour joueur 3
            elif start == 8:
                if col == 0:
                    return True  # chemin trouvé pour joueur 4

            # Vérification des voisins du noeud actuel
            neighbors = []
            if row < self.gridSize-2 and grid[row+1][col].getNature() != 20:
                neighbors.append((row+2, col))

            if row >= 0 and grid[row-1][col].getNature() != 20:
                neighbors.append((row-2, col))

            if col < self.gridSize-2 and grid[row][col+1].getNature() != 10:
                neighbors.append((row, col+2))

            if col >= 0 and grid[row][col-1].getNature() != 10:
                neighbors.append((row, col-2))

            for neighbor in neighbors:
                r, c = neighbor
                if 0 <= r < self.gridSize and 0 <= c < self.gridSize and neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

        return False  # chemin non trouvé pour le joueur

    def displayWinnerPopup(self):
        self.winExitRect = pygame.Rect(
            600, 356, self.cellSize, self.cellSize//2)
        popupsurfaceX = (self.boardSizeX-80*2-self.wallSize*2)/2
        popupsurfaceY = self.boardSizeY/4

        popupSurface = pygame.Surface(
            (popupsurfaceX, popupsurfaceY), pygame.SRCALPHA)
        popupSurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.beige3)
        pygame.draw.rect(popupSurface, popup_color,
                         popupSurface.get_rect(), border_radius=border_radius)
        popupSurfaceRect = popupSurface.get_rect()
        popupSurfaceRect.center = (self.boardSizeX/2, self.boardSizeY/2)

        popupSurface2 = pygame.Surface(
            (popupsurfaceX, popupsurfaceY), pygame.SRCALPHA)
        popupSurface2.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color2 = (self.gray3)

        pygame.draw.rect(popupSurface2, popup_color2,
                         popupSurface2.get_rect(), border_radius=border_radius)
        popupSurfaceRect2 = popupSurface2.get_rect()
        popupSurfaceRect2.center = (
            (self.boardSizeX/2), (self.boardSizeY/2)+self.wallSize//1.5)

        exitSurface = pygame.Surface((80, 80/2))
        exitSurface.fill(self.Red)
        border = pygame.Surface((80, self.wallSize//2))
        border.fill(self.darkRed)

        exitSurfaceRect = exitSurface.get_rect()
        exitSurfaceRect.center = (
            popupsurfaceX/2, popupsurfaceY-80/2)

        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        audioMessage = fontOk.render('OK', True, self.whitheSmoke2)
        audioMessage_rect = audioMessage.get_rect()
        audioMessage_rect.center = ((80//2, (80/2)//2))

        winner = self.currentPlayer-1
        if winner == 0:
            winner = self.nbPlayers
        fontWinner = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        winnerMessage = fontWinner.render("player "+str(
            winner) + " won the game !", True, self.black2)
        winnerMessage_rect = winnerMessage.get_rect()
        winnerMessage_rect.center = (
            (popupsurfaceX/2, ((popupsurfaceY-80/2)//2)))

        winImage = pygame.image.load("assets/images/medal2.png")

        winImage = pygame.transform.smoothscale(
            winImage, (80//2, 80//2))

        winImage_rect = winImage.get_rect()
        winImage_rect.center = (popupsurfaceX//2, 80//4)
        # popupSurface.blit(winImage, winImage_rect)

        exitSurface.blit(audioMessage, audioMessage_rect)
        popupSurface.blit(winnerMessage, winnerMessage_rect)
        popupSurface.blit(exitSurface,  (popupsurfaceX /
                                         2-80/2, popupsurfaceY-self.wallSize*5))
        popupSurface.blit(
            border, (popupsurfaceX/2-80/2,
                     (popupsurfaceY-self.wallSize*5)+80/2))

        self.board.blit(popupSurface2, popupSurfaceRect2)
        self.board.blit(popupSurface, popupSurfaceRect)
        self.screen.blit(self.board, ((self.screenSizeX - self.boardSizeX) //
                         2, (self.screenSizeY - self.boardSizeY) // 2))
        pygame.display.flip()

    def displaySettingsMenu(self):

        self.popupsurfaceX = (self.boardSizeX-80*2-self.wallSize*2)/2
        self.popupsurfaceY = self.boardSizeY/4
        self.popupsurface = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.black)
        pygame.draw.rect(self.popupsurface, popup_color,
                         self.popupsurface.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect = self.popupsurface.get_rect()
        self.popupsurfaceRect.center = (self.boardSizeX/2+(self.screenSizeX - self.boardSizeX) //
                                        2, self.boardSizeY/2)
        self.popupsurface2 = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface2.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color2 = (self.black2)
        pygame.draw.rect(self.popupsurface2, popup_color2,
                         self.popupsurface2.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect2 = self.popupsurface2.get_rect()
        self.popupsurfaceRect2.center = (
            (self.boardSizeX/2)+(self.screenSizeX - self.boardSizeX) //
            2, (self.boardSizeY/2)+self.wallSize//1.5)

        self.sfxRect = pygame.Rect(
            600, 274, 80, 80/2)
        self.sfxSurface = pygame.Surface((80, 80/2))
        borderaudio = pygame.Surface((80, self.wallSize//2))

        if self.sfx == False:
            self.sfxSurface.fill(self.green)
            borderaudio.fill(self.darkGreen)
        if self.sfx == True:
            self.sfxSurface.fill(self.Red)
            borderaudio.fill(self.darkRed)

        self.sfxSurfaceRect = self.sfxSurface.get_rect()
        self.sfxSurfaceRect.center = (
            self.popupsurfaceX/2, self.popupsurfaceY-80/2)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        sfxMessage = fontOk.render('sfx', True, self.whiteSmoke)
        sfxMessage_rect = sfxMessage.get_rect()
        sfxMessage_rect.center = ((80//2, (80/2)//2))
        self.sfxSurface.blit(sfxMessage, sfxMessage_rect)
        self.popupsurface.blit(self.sfxSurface,  (self.popupsurfaceX /
                                                  2-80/2, 10+20))
        self.popupsurface.blit(
            borderaudio, (self.popupsurfaceX/2-80/2,
                          10+80/2+20))

        self.audioRect = pygame.Rect(
            600, 334, 80, 80/2)
        self.audioSurface = pygame.Surface((80, 80/2))
        borderaudio = pygame.Surface((80, self.wallSize//2))
        if self.audio == False:
            self.audioSurface.fill(self.green)
            borderaudio.fill(self.darkGreen)
        if self.audio == True:
            self.audioSurface.fill(self.Red)
            borderaudio.fill(self.darkRed)

        self.audioSurfaceRect = self.audioSurface.get_rect()
        self.audioSurfaceRect.center = (
            self.popupsurfaceX/2, self.popupsurfaceY-80/2)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        audioMessage = fontOk.render('audio', True, self.whiteSmoke)
        audioMessage_rect = audioMessage.get_rect()
        audioMessage_rect.center = ((80//2, (80/2)//2))
        self.audioSurface.blit(audioMessage, audioMessage_rect)
        self.popupsurface.blit(self.audioSurface,  (self.popupsurfaceX /
                                                    2-80/2, 10+80/2+self.wallSize//2+self.wallSize+25))
        self.popupsurface.blit(
            borderaudio, (self.popupsurfaceX/2-80/2,
                          10+80/2+self.wallSize//2+self.wallSize+80/2+25))

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        pygame.display.update()

    def closeWindow(self):
        pygame.quit()
        sys.exit()

    def run(self):
        # sylvie_248
        pygame.init()
        pygamepopup.init()
        self.drawCellHeight()
        self.displayScreen()
        while self.running:
            while not self.checkWin():
                player = "player " + str(self.currentPlayer)
                if self.infosPlayers[player]["nature"] == "human":
                    self.handlingEvents()
                    self.displayScreen()
                    self.drawPlayerDirection()
                    self.displayHover()
                    if self.ShowSettingsMenu == True:
                        self.displaySettingsMenu()
                    pygame.display.flip()
                    self.clock.tick(30)
                if self.infosPlayers[player]["nature"] == "bot":
                    validAction = False
                    while (validAction == False):
                        x = random.randint(0, self.gridSize-2)
                        y = random.randint(0, self.gridSize-2)
                        # approche basée sur des poids
                        # plus la grille est grande plus il faut monter le poids de l'option movepawn
                        option_a_weight = 80
                        option_b_weight = 1

                        total_weight = option_a_weight + option_b_weight
                        random_num = random.uniform(0, total_weight)

                        if random_num < option_a_weight:
                            # l'option A est choisie
                            self.movePawn(x, y)
                        else:
                            # l'option B est choisie
                            self.placeWall(x, y)

                        validAction = True

                    self.displayScreen()
                    pygame.display.flip()
                    self.clock.tick(30)
            self.displayWinnerPopup()
            self.handlingEvents()
        self.displayWinner()


pygame.init()
game = jeu()
game.run()
