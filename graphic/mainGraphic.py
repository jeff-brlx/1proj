import socket
import pickle
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
import threading


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

        self.player_id = 0
        self.played = True

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
        self.darkBrown = (76, 47, 44)
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
        self.totalHuman = 1
        self.totalBot = 1
        self.nbPlayers = self.totalHuman+self.totalBot  # human+bot

        self.infosPlayers = {}
        # Création d'un dictionnaire pour stocker les informations sur chaque joueur
        for i in range(1, self.totalHuman + 1):
            self.infosPlayers[f'player {i}'] = {'nature': 'human'}

        for i in range(self.totalHuman + 1, self.nbPlayers + 1):
            self.infosPlayers[f'player {i}'] = {'nature': 'bot'}

        self.currentPlayer = random.randint(1, self.nbPlayers)

        self.gridSize = 5

        self.fakeGridSize = self.gridSize
        self.gridSize = self.gridSize*2-1

        # choix du nombre de barrières
        if self.fakeGridSize == 11:
            self.nbBarrierPerPlayer = 5

        elif self.fakeGridSize == 9:
            self.nbBarrierPerPlayer = 6

        elif self.fakeGridSize == 7:
            self.nbBarrierPerPlayer = 7

        elif self.fakeGridSize == 5:
            self.nbBarrierPerPlayer = 8

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
                        # barrières "parasites"
                        self.grid[i][j].setNature(7)

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
                        # barrières "parasites"
                        self.grid[i][j].setNature(7)

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
                        self.grid[i][j].setNature(
                            7)  # barrières "parasites

        self.wallSize = 10

        # variables qui servent à améliorer l'affichage graphique
        self.cellSize = None
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

        self.nbBarrierPerPlayer = 4

        # initialisation du nombre de barrières des joueurs

        self.player1barriers = self.nbBarrierPerPlayer
        self.player2barriers = self.nbBarrierPerPlayer
        self.player3barriers = self.nbBarrierPerPlayer
        self.player4Barriers = self.nbBarrierPerPlayer

        self.gameRunning = True
        self.menuRunning = True

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

        # moveSong
        self.audio = True
        self.sfx = True
        self.ShowSettingsMenu = False

        self.moveSong = pygame.mixer.Sound(
            'assets\sounds\MenuSelectionClick.wav')
        self.wallSong = pygame.mixer.Sound(
            'assets/sounds/nutfall.wav')
        self.selectionSong = pygame.mixer.Sound(
            'assets\sounds\selection_sound.mp3')
        self.gameSong = pygame.mixer.Sound(
            'assets\sounds\in-game_music1.mp3')

        self.currentMenu = "menuPrincipal"

        self.playRect = None
        self.rulesRect = None

        self.backRect = None
        self.nextRect = None

        self.lanRect = None
        self.hotSeatRect = None

        self.hostRect = None
        self.joinRect = None

        self.addWallRect = None
        self.deleteWallRect = None

        self.fiveSizeRect = None
        self.sevenSizeRect = None
        self.nineSizeRect = None
        self.elevenSizeRect = None

        self.oneHumanRect = None
        self.twoHumanRect = None
        self.threeHumanRect = None
        self.fourHumanRect = None
        self.zeroBotRect = None
        self.oneBotRect = None
        self.twoBotRect = None
        self.threeBotRect = None

        self.launchPartyRect = None

        self.lan = False
        self.breakParty = False

        self.erase = pygame.Surface(
            (1280, 650))

    def handlingGameEvents(self):  # gestion des évènements

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameRunning = False
                self.closeWindow()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.exitRect.collidepoint(pos):
                    self.playSelectionSong()
                    self.board.fill(self.Brown)
                    self.player3 = False
                    self.player4 = False
                    self.gameRunning = False
                    self.menuRunning = True
                    self.currentMenu = "menuPrincipal"
                    self.runMenu()

                if self.settingsRect.collidepoint(pos):
                    self.playSelectionSong()
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
                            self.playSelectionSong()
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
                            self.playSelectionSong()
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
                        self.playSelectionSong()
                        self.board.fill(self.Brown)
                        self.player3 = False
                        self.player4 = False
                        self.gameRunning = False
                        self.menuRunning = True
                        self.currentMenu = "menuPrincipal"
                        self.runMenu()

                # après un click de souris sur le plateau les coordonnées de grille correspondantes moveSongt générées
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
                    return self.handlingGameEvents()

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
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 4 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 4 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 4 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière )
                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 4 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 4 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(4)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                        if self.currentPlayer == 2:
                            # déplacments normaux (gauche , droite , haut , bat)
                            # verticale
                            if self.grid[y][x-2].getNature() == 5 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 5 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 5 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 5 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière  )
                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 5 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 5 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(5)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                        if self.currentPlayer == 3:
                            # déplacments normaux (gauche , droite , haut , bat)
                            if self.grid[y][x-2].getNature() == 6 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 6 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 6 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 6 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière  )
                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 6 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 6 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(6)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                        if self.currentPlayer == 4:
                            # déplacments normaux (gauche , droite , haut , bat)
                            if self.grid[y][x-2].getNature() == 8 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+2].getNature() == 8 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+2][x].getNature() == 8 and self.grid[y+1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-2][x].getNature() == 8 and self.grid[y-1][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # saut de pions
                            if self.grid[y][x-4].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y][x-1].getNature() == 2 and self.grid[y][x-3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x-4].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y][x+4].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y][x+1].getNature() == 2 and self.grid[y][x+3].getNature() == 2 and self.grid[y][x].getNature() == 0:
                                self.grid[y][x+4].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y-4][x].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-1][x].getNature() == 1 and self.grid[y-3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y-4][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            if self.grid[y+4][x].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+1][x].getNature() == 1 and self.grid[y+3][x].getNature() == 1 and self.grid[y][x].getNature() == 0:
                                self.grid[y+4][x].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacements en diagonale ( pion adverse + barrière  )
                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y-1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y-1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y+1][x+2].getNature() == 20 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y+1][x-2].getNature() == 20 and self.grid[y][x-1].getNature() != 10 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+1].getNature() == 10 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-1].getNature() == 10 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            # déplacement en diagonale ( pion adverse + pion adverse )
                            # verticale
                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y][x+2].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y][x+1].getNature() != 10 and self.grid[y-1][x+2].getNature() != 20 and self.grid[y+1][x+2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y][x-2].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y][x-1].getNature() != 10 and self.grid[y+1][x-2].getNature() != 20 and self.grid[y-1][x-2].getNature() != 20 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return
                            # Horizontale
                            if self.grid[y-2][x-2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x+2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y-2][x+2].getNature() == 8 and self.grid[y-2][x].getNature() != 0 and self.grid[y-2][x-2].getNature() != 0 and self.grid[y-1][x].getNature() != 20 and self.grid[y-2][x-1].getNature() != 10 and self.grid[y-2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y-2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x-2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x+2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x-2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

                            if self.grid[y+2][x+2].getNature() == 8 and self.grid[y+2][x].getNature() != 0 and self.grid[y+2][x-2].getNature() != 0 and self.grid[y+1][x].getNature() != 20 and self.grid[y+2][x-1].getNature() != 10 and self.grid[y+2][x+1].getNature() != 10 and self.grid[y][x].getNature() == 0:
                                self.grid[y+2][x+2].setNature(0)
                                self.grid[y][x].setNature(8)
                                self.playMoveSong()
                                self.nextPlayer()
                                return

    def placeWall(self, x, y):
        if self.ShowSettingsMenu == False:
            # clique à la limite droite du tableau
            while (x == self.gridSize-1):
                return self.handlingGameEvents()

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
                                    self.playWallSong()
                                    self.played = True
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
                                    self.playWallSong()
                                    self.played = True
                                    self.nextPlayer()
                                    return

    def verifyPath(self, gridCopy):
        # vérification des chemins
        if self.nbPlayers == 2:
            if self.pathFinding(4, self.grid) is False or self.pathFinding(5, self.grid) is False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = copy.deepcopy(gridCopy)
                self.warning()
                print("impossible to place this wall . Please try again")

            else:
                return True

        elif self.nbPlayers == 3:
            if self.pathFinding(4, self.grid) is False or self.pathFinding(5, self.grid) is False or self.pathFinding(6, self.grid) is False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = copy.deepcopy(gridCopy)
                self.warning()
                print("impossible to place this wall . Please try again")

            else:
                return True

        elif self.nbPlayers == 4:
            if self.pathFinding(4, self.grid) is False or self.pathFinding(5, self.grid) is False or self.pathFinding(6, self.grid) is False or self.pathFinding(8, self.grid) is False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = copy.deepcopy(gridCopy)
                self.warning()
                print("impossible to place this wall . Please try again")

            else:
                return True

    def playMoveSong(self):
        if self.sfx == True:
            self.moveSong.play()
            # Attendre la fin de la lecture du son
            pygame.time.wait(int(self.moveSong.get_length() * 1000))
            self.moveSong.stop()

    def playWallSong(self):
        if self.sfx == True:
            self.wallSong.play()
            # Attendre la fin de la lecture du son
            pygame.time.wait(int(self.wallSong.get_length() * 1000))
            self.wallSong.stop()

    def playSelectionSong(self):
        if self.sfx == True:
            self.selectionSong.play()
            # Attendre la fin de la lecture du son
            pygame.time.wait(int(self.selectionSong.get_length() * 1000))
            self.selectionSong.stop()

    def playGameSong(self):
        if self.audio == True:
            self.gameSong.play()

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
        return self.handlingGameEvents()

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

        if self.sfx == True:
            self.sfxSurface.fill(self.green)
            borderaudio.fill(self.darkGreen)
        if self.sfx == False:
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
        if self.audio == True:
            self.audioSurface.fill(self.green)
            borderaudio.fill(self.darkGreen)
        if self.audio == False:
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

    def handlingMenuEvent(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameRunning = False
                self.closeWindow()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if self.addWallRect:
                    if self.addWallRect.collidepoint(pos):
                        self.playSelectionSong()
                        if self.gridSize == 5*2-1:
                            if 4 <= self.nbBarrierPerPlayer+4 <= 16:
                                self.nbBarrierPerPlayer += 4
                        if self.gridSize == 7*2-1:
                            if 4 <= self.nbBarrierPerPlayer+4 <= 24:
                                self.nbBarrierPerPlayer += 4
                        if self.gridSize == 9*2-1:
                            if 4 <= self.nbBarrierPerPlayer+4 <= 32:
                                self.nbBarrierPerPlayer += 4
                        if self.gridSize == 11*2-1:
                            if 4 <= self.nbBarrierPerPlayer+4 <= 40:
                                self.nbBarrierPerPlayer += 4
                        self.menu4()

                if self.deleteWallRect:
                    if self.deleteWallRect.collidepoint(pos):
                        self.playSelectionSong()
                        if self.gridSize == 5*2-1:
                            if 4 <= self.nbBarrierPerPlayer-4 <= 16:
                                self.nbBarrierPerPlayer -= 4
                        if self.gridSize == 7*2-1:
                            if 4 <= self.nbBarrierPerPlayer-4 <= 24:
                                self.nbBarrierPerPlayer -= 4
                        if self.gridSize == 9*2-1:
                            if 4 <= self.nbBarrierPerPlayer-4 <= 32:
                                self.nbBarrierPerPlayer -= 4
                        if self.gridSize == 11*2-1:
                            if 4 <= self.nbBarrierPerPlayer-4 <= 40:
                                self.nbBarrierPerPlayer -= 4
                        self.menu4()

                if self.playRect:
                    if self.playRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.currentMenu = "hotseatOrLan"

                if self.lanRect:
                    if self.lanRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.lan = True

                        self.currentMenu = "hostOrJoin"

                if self.hotSeatRect:
                    if self.hotSeatRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.currentMenu = "board&barrier"

                if self.hostRect:
                    if self.hostRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.currentMenu = "board&barrier"

                if self.joinRect:
                    if self.joinRect.collidepoint(pos):
                        self.playSelectionSong()
                        # self.currentMenu = "join"
                        self.client()

                if self.fiveSizeRect:
                    if self.fiveSizeRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.gridSize = 5*2-1
                        self.fakeGridSize = 5
                        self.cellSize = 80
                        self.pawnShadow = 4
                        self.pawnRadius = self.wallSize//2
                        self.settingX = 860
                        if self.nbBarrierPerPlayer > 16:
                            self.nbBarrierPerPlayer = 16
                        self.menu4()

                if self.sevenSizeRect:
                    if self.sevenSizeRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.gridSize = 7*2-1
                        self.fakeGridSize = 7
                        self.cellSize = 60
                        self.pawnShadow = 4
                        self.pawnRadius = self.wallSize//2
                        self.settingX = 880
                        if self.nbBarrierPerPlayer > 24:
                            self.nbBarrierPerPlayer = 24

                        self.menu4()

                if self.nineSizeRect:
                    if self.nineSizeRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.gridSize = 9*2-1
                        self.fakeGridSize = 9
                        self.cellSize = 50
                        self.pawnShadow = 3
                        self.pawnRadius = self.wallSize//2
                        self.settingX = 920
                        if self.nbBarrierPerPlayer > 32:
                            self.nbBarrierPerPlayer = 32
                        self.menu4()

                if self.elevenSizeRect:
                    if self.elevenSizeRect.collidepoint(pos):
                        self.playSelectionSong()
                        self.gridSize = 11*2-1
                        self.fakeGridSize = 11
                        self.cellSize = 40
                        self.pawnShadow = 3
                        self.pawnRadius = 4
                        self.settingX = 920
                        self.menu4()

                if self.oneHumanRect:
                    if self.oneHumanRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 1+self.totalBot <= 4:
                            self.totalHuman = 1
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()
                if self.twoHumanRect:
                    if self.twoHumanRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 2+self.totalBot <= 4:
                            self.totalHuman = 2
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()
                if self.threeHumanRect:
                    if self.threeHumanRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 3+self.totalBot <= 4:
                            self.totalHuman = 3
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()
                if self.fourHumanRect:
                    if self.fourHumanRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 4+self.totalBot <= 4:
                            self.totalHuman = 4
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()

                if self.zeroBotRect:
                    if self.zeroBotRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 0+self.totalHuman <= 4:
                            self.totalBot = 0
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()
                if self.oneBotRect:
                    if self.oneBotRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 1+self.totalHuman <= 4:
                            self.totalBot = 1
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()
                if self.twoBotRect:
                    if self.twoBotRect.collidepoint(pos):
                        if 2+self.totalHuman <= 4:
                            self.totalBot = 2
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()
                if self.threeBotRect:
                    if self.threeBotRect.collidepoint(pos):
                        self.playSelectionSong()
                        if 3+self.totalHuman <= 4:
                            self.totalBot = 3
                            self.nbPlayers = self.totalHuman+self.totalBot
                        self.menu5()

                if self.nextRect:

                    if self.nextRect.collidepoint(pos):
                        self.playSelectionSong()
                        if self.currentMenu == "board&barrier":
                            self.currentMenu = "humanOrBot"

                if self.launchPartyRect:
                    if self.launchPartyRect.collidepoint(pos):
                        self.playSelectionSong()
                        if self.lan == True:
                            # self.currentMenu = "join"
                            self.currentPlayer = random.randint(
                                1, self.nbPlayers)
                            self.startServer()

                        elif self.lan == False:
                            if self.currentMenu == "humanOrBot":
                                self.menuRunning = False
                                self.majVariables()
                                self.run()

                if self.backRect:
                    if self.backRect.collidepoint(pos):
                        self.playSelectionSong()

                        if self.currentMenu == "rules":
                            self.currentMenu = "menuPrincipal"
                        if self.currentMenu == "hotseatOrLan":
                            self.currentMenu = "menuPrincipal"
                        if self.currentMenu == "hostOrJoin":
                            self.lan = False
                            self.currentMenu = "hotseatOrLan"

                        if self.currentMenu == "board&barrier":
                            if self.lan == False:
                                self.currentMenu = "hotseatOrLan"
                            if self.lan == True:
                                self.currentMenu = "hostOrJoin"

                        if self.currentMenu == "humanOrBot":
                            self.currentMenu = "board&barrier"

    def run(self):
        # sylvie_248
        self.drawCellHeight()
        self.displayScreen()
        while self.gameRunning:
            while not self.checkWin():
                player = "player " + str(self.currentPlayer)
                if self.infosPlayers[player]["nature"] == "human":
                    self.handlingGameEvents()
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
            self.handlingGameEvents()
            self.screen.fill(0, 0, 0)
            pygame.display.flip()

    def warning(self):

        self.popupsurfaceX = (self.boardSizeX-80-self.wallSize*2)/2
        self.popupsurfaceY = self.boardSizeY/8
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

        warningFont = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        warningMessage = warningFont.render(
            'Impossible action. Please try again', True, self.whiteSmoke)
        warningMessage_rect = warningMessage.get_rect()
        warningMessage_rect.center = (
            (self.popupsurfaceX//2, self.popupsurfaceY//2+10))
        self.popupsurface.blit(warningMessage, warningMessage_rect)

        warningImage = pygame.image.load(
            "assets\images\warning.webp").convert_alpha()
        warningImage = pygame.transform.scale(
            warningImage, (25, 25))
        warningImage_rect = warningImage.get_rect()
        warningImage_rect.center = (self.popupsurfaceX//2, 25)

        self.popupsurface.blit(warningImage, warningImage_rect)
        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        pygame.display.update()

    def displayMenus(self):

        if self.currentMenu == "menuPrincipal":

            self.backRect = None
            self.nextRect = None
            self.lanRect = None
            self.hotSeatRect = None
            self.hostRect = None
            self.joinRect = None
            self.addWallRect = None
            self.deleteWallRect = None
            self.fiveSizeRect = None
            self.sevenSizeRect = None
            self.nineSizeRect = None
            self.elevenSizeRect = None
            self.launchPartyRect = None
            self.oneHumanRect = None
            self.twoHumanRect = None
            self.threeHumanRect = None
            self.fourHumanRect = None
            self.zeroBotRect = None
            self.oneBotRect = None
            self.twoBotRect = None
            self.threeBotRect = None
            self.menu1()

        if self.currentMenu == "hotseatOrLan":

            self.playRect = None
            self.rulesRect = None
            self.backRect = None
            self.nextRect = None
            self.hostRect = None
            self.joinRect = None
            self.addWallRect = None
            self.deleteWallRect = None
            self.fiveSizeRect = None
            self.sevenSizeRect = None
            self.nineSizeRect = None
            self.elevenSizeRect = None
            self.launchPartyRect = None
            self.oneHumanRect = None
            self.twoHumanRect = None
            self.threeHumanRect = None
            self.fourHumanRect = None
            self.zeroBotRect = None
            self.oneBotRect = None
            self.twoBotRect = None
            self.threeBotRect = None
            self.menu2()

        if self.currentMenu == "hostOrJoin":

            self.playRect = None
            self.rulesRect = None
            self.backRect = None
            self.nextRect = None
            self.lanRect = None
            self.hotSeatRect = None
            self.addWallRect = None
            self.deleteWallRect = None
            self.fiveSizeRect = None
            self.sevenSizeRect = None
            self.nineSizeRect = None
            self.elevenSizeRect = None
            self.launchPartyRect = None
            self.oneHumanRect = None
            self.twoHumanRect = None
            self.threeHumanRect = None
            self.fourHumanRect = None
            self.zeroBotRect = None
            self.oneBotRect = None
            self.twoBotRect = None
            self.threeBotRect = None
            self.menu3()

        if self.currentMenu == "board&barrier":

            self.playRect = None
            self.rulesRect = None
            self.backRect = None
            self.nextRect = None
            self.lanRect = None
            self.hotSeatRect = None
            self.hostRect = None
            self.joinRect = None
            self.launchPartyRect = None
            self.oneHumanRect = None
            self.twoHumanRect = None
            self.threeHumanRect = None
            self.fourHumanRect = None
            self.zeroBotRect = None
            self.oneBotRect = None
            self.twoBotRect = None
            self.threeBotRect = None
            self.menu4()

        if self.currentMenu == "humanOrBot":

            self.playRect = None
            self.rulesRect = None
            self.backRect = None
            self.nextRect = None
            self.lanRect = None
            self.hotSeatRect = None
            self.hostRect = None
            self.joinRect = None
            self.addWallRect = None
            self.deleteWallRect = None
            self.fiveSizeRect = None
            self.sevenSizeRect = None
            self.nineSizeRect = None
            self.elevenSizeRect = None
            self.oneHumanRect = None
            self.twoHumanRect = None
            self.threeHumanRect = None
            self.fourHumanRect = None
            self.zeroBotRect = None
            self.oneBotRect = None
            self.twoBotRect = None
            self.threeBotRect = None
            self.menu5()

    def menu1(self):

        self.screen.fill(self.beige6)
        self.popupsurfaceX = 500
        self.popupsurfaceY = 400
        self.popupsurface = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.Brown)
        pygame.draw.rect(self.popupsurface, popup_color,
                         self.popupsurface.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect = self.popupsurface.get_rect()
        self.popupsurfaceRect.center = (self.boardSizeX/2+(self.screenSizeX - self.boardSizeX) //
                                        2, self.boardSizeY/2)
        self.popupsurface2 = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface2.fill((0, 0, 0, 0))

        border_radius = 10
        popup_color2 = (self.darkBrown
                        )
        pygame.draw.rect(self.popupsurface2, popup_color2,
                         self.popupsurface2.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect2 = self.popupsurface2.get_rect()
        self.popupsurfaceRect2.center = (
            (self.boardSizeX/2)+(self.screenSizeX - self.boardSizeX) //
            2, (self.boardSizeY/2)+self.wallSize//1.5+6)

        # PLAY SURFACE
        self.playButtonX = 200
        self.playButtonY = 75

        self.playRect = pygame.Rect(
            540, 202, self.playButtonX, self.playButtonY)

        self.playSurface = pygame.Surface((self.playButtonX, self.playButtonY))
        borderplay = pygame.Surface((self.playButtonX, 5+self.playButtonY))

        self.playSurface.fill(self.black)
        borderplay.fill(self.black2)

        self.playSurfaceRect = self.playSurface.get_rect()
        self.playSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playMessage = fontOk.render('play', True, self.whiteSmoke)
        playMessage_rect = playMessage.get_rect()
        playMessage_rect.center = (
            (self.playButtonX//2, (self.playButtonY)//2))
        self.playSurface.blit(playMessage, playMessage_rect)
        self.popupsurface.blit(
            borderplay, self.playSurfaceRect)
        self.popupsurface.blit(self.playSurface,  self.playSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # RULES SURFACE
        self.rulesButtonX = 200
        self.rulesButtonY = 75

        self.rulesRect = pygame.Rect(
            540, 334, self.rulesButtonX, self.rulesButtonY)

        self.rulesSurface = pygame.Surface(
            (self.rulesButtonX, self.rulesButtonY))
        borderrules = pygame.Surface((self.rulesButtonX, 5+self.rulesButtonY))

        self.rulesSurface.fill(self.black)
        borderrules.fill(self.black2)

        self.rulesSurfaceRect = self.rulesSurface.get_rect()
        self.rulesSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//3)*2-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        rulesMessage = fontOk.render('Rules', True, self.whiteSmoke)
        rulesMessage_rect = rulesMessage.get_rect()
        rulesMessage_rect.center = (
            (self.rulesButtonX//2, (self.rulesButtonY)//2))
        self.rulesSurface.blit(rulesMessage, rulesMessage_rect)
        self.popupsurface.blit(
            borderrules, self.rulesSurfaceRect)
        self.popupsurface.blit(self.rulesSurface,  self.rulesSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        pygame.display.update()

    def menu2(self):
        # MENU SURFACE
        self.screen.fill(self.beige6)
        self.popupsurfaceX = 500
        self.popupsurfaceY = 400
        self.popupsurface = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.Brown)
        pygame.draw.rect(self.popupsurface, popup_color,
                         self.popupsurface.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect = self.popupsurface.get_rect()
        self.popupsurfaceRect.center = (self.boardSizeX/2+(self.screenSizeX - self.boardSizeX) //
                                        2, self.boardSizeY/2)
        self.popupsurface2 = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface2.fill((0, 0, 0, 0))

        border_radius = 10
        popup_color2 = (self.darkBrown
                        )
        pygame.draw.rect(self.popupsurface2, popup_color2,
                         self.popupsurface2.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect2 = self.popupsurface2.get_rect()
        self.popupsurfaceRect2.center = (
            (self.boardSizeX/2)+(self.screenSizeX - self.boardSizeX) //
            2, (self.boardSizeY/2)+self.wallSize//1.5+6)

        # BACK SURFACE
        self.backRect = pygame.Rect(
            600, 468, 80, 80/2)
        self.backSurface = pygame.Surface((80, 80/2))
        bordernext = pygame.Surface((80, 5+80/2))

        self.backSurface.fill(self.Red)
        bordernext.fill(self.darkRed)

        self.backSurfaceRect = self.backSurface.get_rect()
        self.backSurfaceRect.center = (
            self.popupsurfaceX//2, (self.popupsurfaceY//12)*11)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 16)
        backMessage = fontOk.render('Back', True, self.whiteSmoke)
        backMessage_rect = backMessage.get_rect()
        backMessage_rect.center = ((80//2, (80/2)//2))
        self.backSurface.blit(backMessage, backMessage_rect)
        self.popupsurface.blit(
            bordernext,
            self.backSurfaceRect)
        self.popupsurface.blit(self.backSurface,  self.backSurfaceRect)

        # hotSeat SURFACE
        self.hotSeatButtonX = 200
        self.hotSeatButtonY = 75

        self.hotSeatRect = pygame.Rect(
            540, 202, self.hotSeatButtonX, self.hotSeatButtonY)

        self.hotSeatSurface = pygame.Surface(
            (self.hotSeatButtonX, self.hotSeatButtonY))
        borderhotSeat = pygame.Surface(
            (self.hotSeatButtonX, 5+self.hotSeatButtonY))

        self.hotSeatSurface.fill(self.black)
        borderhotSeat.fill(self.black2)

        self.hotSeatSurfaceRect = self.hotSeatSurface.get_rect()
        self.hotSeatSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        hotSeatMessage = fontOk.render('Hotseat Party', True, self.whiteSmoke)
        hotSeatMessage_rect = hotSeatMessage.get_rect()
        hotSeatMessage_rect.center = (
            (self.hotSeatButtonX//2, (self.hotSeatButtonY)//2))
        self.hotSeatSurface.blit(hotSeatMessage, hotSeatMessage_rect)
        self.popupsurface.blit(
            borderhotSeat, self.hotSeatSurfaceRect)
        self.popupsurface.blit(self.hotSeatSurface,  self.hotSeatSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # lan SURFACE
        self.lanButtonX = 200
        self.lanButtonY = 75

        self.lanRect = pygame.Rect(
            540, 334, self.lanButtonX, self.lanButtonY)

        self.lanSurface = pygame.Surface(
            (self.lanButtonX, self.lanButtonY))
        borderlan = pygame.Surface((self.lanButtonX, 5+self.lanButtonY))

        self.lanSurface.fill(self.black)
        borderlan.fill(self.black2)

        self.lanSurfaceRect = self.lanSurface.get_rect()
        self.lanSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//3)*2-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        lanMessage = fontOk.render('Lan Party', True, self.whiteSmoke)
        lanMessage_rect = lanMessage.get_rect()
        lanMessage_rect.center = (
            (self.lanButtonX//2, (self.lanButtonY)//2))
        self.lanSurface.blit(lanMessage, lanMessage_rect)
        self.popupsurface.blit(
            borderlan, self.lanSurfaceRect)
        self.popupsurface.blit(self.lanSurface,  self.lanSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        pygame.display.update()

    def menu3(self):
        # MENU SURFACE
        self.screen.fill(self.beige6)
        self.popupsurfaceX = 500
        self.popupsurfaceY = 400
        self.popupsurface = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.Brown)
        pygame.draw.rect(self.popupsurface, popup_color,
                         self.popupsurface.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect = self.popupsurface.get_rect()
        self.popupsurfaceRect.center = (self.boardSizeX/2+(self.screenSizeX - self.boardSizeX) //
                                        2, self.boardSizeY/2)
        self.popupsurface2 = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface2.fill((0, 0, 0, 0))

        border_radius = 10
        popup_color2 = (self.darkBrown
                        )
        pygame.draw.rect(self.popupsurface2, popup_color2,
                         self.popupsurface2.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect2 = self.popupsurface2.get_rect()
        self.popupsurfaceRect2.center = (
            (self.boardSizeX/2)+(self.screenSizeX - self.boardSizeX) //
            2, (self.boardSizeY/2)+self.wallSize//1.5+6)

        # BACK SURFACE
        self.backRect = pygame.Rect(
            600, 468, 80, 80/2)
        self.backSurface = pygame.Surface((80, 80/2))
        bordernext = pygame.Surface((80, 5+80/2))

        self.backSurface.fill(self.Red)
        bordernext.fill(self.darkRed)

        self.backSurfaceRect = self.backSurface.get_rect()
        self.backSurfaceRect.center = (
            self.popupsurfaceX//2, (self.popupsurfaceY//12)*11)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 16)
        backMessage = fontOk.render('Back', True, self.whiteSmoke)
        backMessage_rect = backMessage.get_rect()
        backMessage_rect.center = ((80//2, (80/2)//2))
        self.backSurface.blit(backMessage, backMessage_rect)
        self.popupsurface.blit(
            bordernext,
            self.backSurfaceRect)
        self.popupsurface.blit(self.backSurface,  self.backSurfaceRect)

        # host SURFACE
        self.hostButtonX = 200
        self.hostButtonY = 75

        self.hostRect = pygame.Rect(
            540, 202, self.hostButtonX, self.hostButtonY)

        self.hostSurface = pygame.Surface((self.hostButtonX, self.hostButtonY))
        borderhost = pygame.Surface((self.hostButtonX, 5+self.hostButtonY))

        self.hostSurface.fill(self.black)
        borderhost.fill(self.black2)

        self.hostSurfaceRect = self.hostSurface.get_rect()
        self.hostSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        hostMessage = fontOk.render('Host', True, self.whiteSmoke)
        hostMessage_rect = hostMessage.get_rect()
        hostMessage_rect.center = (
            (self.hostButtonX//2, (self.hostButtonY)//2))
        self.hostSurface.blit(hostMessage, hostMessage_rect)
        self.popupsurface.blit(
            borderhost, self.hostSurfaceRect)
        self.popupsurface.blit(self.hostSurface,  self.hostSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # join SURFACE
        self.joinButtonX = 200
        self.joinButtonY = 75

        self.joinRect = pygame.Rect(
            540, 334, self.joinButtonX, self.joinButtonY)

        self.joinSurface = pygame.Surface(
            (self.joinButtonX, self.joinButtonY))
        borderjoin = pygame.Surface((self.joinButtonX, 5+self.joinButtonY))

        self.joinSurface.fill(self.black)
        borderjoin.fill(self.black2)

        self.joinSurfaceRect = self.joinSurface.get_rect()
        self.joinSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//3)*2-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        joinMessage = fontOk.render('Join', True, self.whiteSmoke)
        joinMessage_rect = joinMessage.get_rect()
        joinMessage_rect.center = (
            (self.joinButtonX//2, (self.joinButtonY)//2))
        self.joinSurface.blit(joinMessage, joinMessage_rect)
        self.popupsurface.blit(
            borderjoin, self.joinSurfaceRect)
        self.popupsurface.blit(self.joinSurface,  self.joinSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        pygame.display.update()

    def menu4(self):
        # MENU SURFACE
        self.screen.fill(self.beige6)
        self.popupsurfaceX = 500
        self.popupsurfaceY = 470
        self.popupsurface = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.Brown)
        pygame.draw.rect(self.popupsurface, popup_color,
                         self.popupsurface.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect = self.popupsurface.get_rect()
        self.popupsurfaceRect.center = (self.boardSizeX/2+(self.screenSizeX - self.boardSizeX) //
                                        2, self.boardSizeY/2)
        self.popupsurface2 = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface2.fill((0, 0, 0, 0))

        border_radius = 10
        popup_color2 = (self.darkBrown
                        )
        pygame.draw.rect(self.popupsurface2, popup_color2,
                         self.popupsurface2.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect2 = self.popupsurface2.get_rect()
        self.popupsurfaceRect2.center = (
            (self.boardSizeX/2)+(self.screenSizeX - self.boardSizeX) //
            2, (self.boardSizeY/2)+self.wallSize//1.5+6)

        # BACK SURFACE
        self.backRect = pygame.Rect(
            517, 500, 80, 80/2)
        self.backSurface = pygame.Surface((80, 80/2))
        bordernext = pygame.Surface((80, 5+80/2))

        self.backSurface.fill(self.Red)
        bordernext.fill(self.darkRed)

        self.backSurfaceRect = self.backSurface.get_rect()
        self.backSurfaceRect.center = (
            self.popupsurfaceX//3, (self.popupsurfaceY//12)*11)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        backMessage = fontOk.render('Back', True, self.whiteSmoke)
        backMessage_rect = backMessage.get_rect()
        backMessage_rect.center = ((80//2, (80/2)//2))
        self.backSurface.blit(backMessage, backMessage_rect)
        self.popupsurface.blit(
            bordernext,
            self.backSurfaceRect)
        self.popupsurface.blit(self.backSurface,  self.backSurfaceRect)

        # NEXT SURFACE
        self.nextRect = pygame.Rect(
            680, 500, 80, 80/2)
        self.nextSurface = pygame.Surface((80, 80/2))
        bordernext = pygame.Surface((80, 5+80/2))

        self.nextSurface.fill(self.green)
        bordernext.fill(self.darkGreen)

        self.nextSurfaceRect = self.nextSurface.get_rect()
        self.nextSurfaceRect.center = (
            (self.popupsurfaceX//3)*2, (self.popupsurfaceY//12)*11)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        nextMessage = fontOk.render('Next', True, self.whiteSmoke)
        nextMessage_rect = nextMessage.get_rect()
        nextMessage_rect.center = ((80//2, (80/2)//2))
        self.nextSurface.blit(nextMessage, nextMessage_rect)
        self.popupsurface.blit(
            bordernext, self.nextSurfaceRect)
        self.popupsurface.blit(self.nextSurface,  self.nextSurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # RULES SURFACE
        self.rulesButtonX = 350
        self.rulesButtonY = 50

        self.rulesSurface = pygame.Surface(
            (self.rulesButtonX, self.rulesButtonY))
        borderrules = pygame.Surface((self.rulesButtonX, 5+self.rulesButtonY))

        self.rulesSurface.fill(self.black)
        borderrules.fill(self.black2)

        self.rulesSurfaceRect = self.rulesSurface.get_rect()
        self.rulesSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//8))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        rulesMessage = fontOk.render('Board size', True, self.whiteSmoke)
        rulesMessage_rect = rulesMessage.get_rect()
        rulesMessage_rect.center = (
            (self.rulesButtonX//2, (self.rulesButtonY)//2))
        self.rulesSurface.blit(rulesMessage, rulesMessage_rect)
        self.popupsurface.blit(
            borderrules, self.rulesSurfaceRect)
        self.popupsurface.blit(self.rulesSurface,  self.rulesSurfaceRect)

        # Player number5 SURFACE
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65

        self.fiveSizeRect = pygame.Rect(
            417, 211, self.playerNbButtonX, self.playerNbButtonY)

        self.playerNbSurface5 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer5Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.gridSize == 5*2-1:
            self.playerNbSurface5.fill(self.blue)
            borderplayer5Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface5.fill(self.beige3)
            borderplayer5Nb.fill(self.gray3)

        self.playerNbSurface5Rect = self.playerNbSurface5.get_rect()
        self.playerNbSurface5Rect.center = (
            (self.popupsurfaceX//8), (self.popupsurfaceY//8)*3-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('5 x 5', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface5.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer5Nb, self.playerNbSurface5Rect)
        self.popupsurface.blit(self.playerNbSurface5,
                               self.playerNbSurface5Rect)

        # Player number 7 Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65

        self.sevenSizeRect = pygame.Rect(
            540, 211, self.playerNbButtonX, self.playerNbButtonY)

        self.playerNbSurface9 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer7Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.gridSize == 7*2-1:
            self.playerNbSurface9.fill(self.blue)
            borderplayer7Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface9.fill(self.beige3)
            borderplayer7Nb.fill(self.gray3)

        self.playerNbSurface9Rect = self.playerNbSurface9.get_rect()
        self.playerNbSurface9Rect.center = (
            (self.popupsurfaceX//8)*3, ((self.popupsurfaceY//8)*3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('7 x 7', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface9.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer7Nb, self.playerNbSurface9Rect)
        self.popupsurface.blit(self.playerNbSurface9,
                               self.playerNbSurface9Rect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # Player number9 SURFACE
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65

        self.nineSizeRect = pygame.Rect(
            664, 211, self.playerNbButtonX, self.playerNbButtonY)

        self.playerNbSurface9 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer9Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.gridSize == 9*2-1:
            self.playerNbSurface9.fill(self.blue)
            borderplayer9Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface9.fill(self.beige3)
            borderplayer9Nb.fill(self.gray3)

        self.playerNbSurface9Rect = self.playerNbSurface9.get_rect()
        self.playerNbSurface9Rect.center = (
            (self.popupsurfaceX//8)*5, ((self.popupsurfaceY//8)*3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('9 x 9', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface9.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer9Nb, self.playerNbSurface9Rect)
        self.popupsurface.blit(self.playerNbSurface9,
                               self.playerNbSurface9Rect)

        # Player number 11 Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65

        self.elevenSizeRect = pygame.Rect(
            789, 211, self.playerNbButtonX, self.playerNbButtonY)

        self.playerNbSurface11 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer11Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.gridSize == 11*2-1:
            self.playerNbSurface11.fill(self.blue)
            borderplayer11Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface11.fill(self.beige3)
            borderplayer11Nb.fill(self.gray3)

        self.playerNbSurface11Rect = self.playerNbSurface11.get_rect()
        self.playerNbSurface11Rect.center = (
            (self.popupsurfaceX//8)*7, ((self.popupsurfaceY//8)*3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('11 x 11', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface11.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer11Nb, self.playerNbSurface11Rect)
        self.popupsurface.blit(self.playerNbSurface11,
                               self.playerNbSurface11Rect)

        # Wall number SURFACE
        self.rulesButtonX = 350
        self.rulesButtonY = 50

        self.rulesSurface = pygame.Surface(
            (self.rulesButtonX, self.rulesButtonY))
        borderrules = pygame.Surface((self.rulesButtonX, 5+self.rulesButtonY))

        self.rulesSurface.fill(self.black)
        borderrules.fill(self.black2)

        self.rulesSurfaceRect = self.rulesSurface.get_rect()
        self.rulesSurfaceRect.center = (
            (self.popupsurfaceX//2), ((self.popupsurfaceY//8)*4)+12)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        rulesMessage = fontOk.render('Walls per player', True, self.whiteSmoke)
        rulesMessage_rect = rulesMessage.get_rect()
        rulesMessage_rect.center = (
            (self.rulesButtonX//2, (self.rulesButtonY)//2))
        self.rulesSurface.blit(rulesMessage, rulesMessage_rect)
        self.popupsurface.blit(
            borderrules, self.rulesSurfaceRect)
        self.popupsurface.blit(self.rulesSurface,  self.rulesSurfaceRect)

        # show wall Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65

        self.playerNbSurface11 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer7Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        self.playerNbSurface11.fill(self.beige3)
        borderplayer7Nb.fill(self.gray3)

        self.playerNbSurface11Rect = self.playerNbSurface11.get_rect()
        self.playerNbSurface11Rect.center = (
            (self.popupsurfaceX//6)*3, ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render(
            str(self.nbBarrierPerPlayer), True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface11.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer7Nb, self.playerNbSurface11Rect)
        self.popupsurface.blit(self.playerNbSurface11,
                               self.playerNbSurface11Rect)

        # delete wall Surface
        self.playerNbButtonX = 70//3
        self.playerNbButtonY = 65//3

        self.deleteWallRect = pygame.Rect(
            545, 416, 70//3, 65//3)

        self.playerNbSurface11 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer7Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        self.playerNbSurface11.fill(self.blue)
        borderplayer7Nb.fill(self.darkBlue)

        self.playerNbSurface11Rect = self.playerNbSurface11.get_rect()
        self.playerNbSurface11Rect.center = (
            (self.popupsurfaceX//6)*2, ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render("-", True, self.whiteSmoke)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface11.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer7Nb, self.playerNbSurface11Rect)
        self.popupsurface.blit(self.playerNbSurface11,
                               self.playerNbSurface11Rect)

        # add wall Surface
        self.playerNbButtonX = 70//3
        self.playerNbButtonY = 65//3

        self.addWallRect = pygame.Rect(
            711, 416, 70//3, 65//3)

        self.playerNbSurface11 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer7Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        self.playerNbSurface11.fill(self.blue)
        borderplayer7Nb.fill(self.darkBlue)

        self.playerNbSurface11Rect = self.playerNbSurface11.get_rect()
        self.playerNbSurface11Rect.center = (
            (self.popupsurfaceX//6)*4, ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render("+", True, self.whiteSmoke)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface11.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer7Nb, self.playerNbSurface11Rect)
        self.popupsurface.blit(self.playerNbSurface11,
                               self.playerNbSurface11Rect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)
        pygame.display.update()

    def menu5(self):
        # MENU SURFACE
        self.screen.fill(self.beige6)
        self.popupsurfaceX = 500
        self.popupsurfaceY = 470
        self.popupsurface = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface.fill((0, 0, 0, 0))
        border_radius = 10
        popup_color = (self.Brown)
        pygame.draw.rect(self.popupsurface, popup_color,
                         self.popupsurface.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect = self.popupsurface.get_rect()
        self.popupsurfaceRect.center = (self.boardSizeX/2+(self.screenSizeX - self.boardSizeX) //
                                        2, self.boardSizeY/2)
        self.popupsurface2 = pygame.Surface(
            (self.popupsurfaceX, self.popupsurfaceY), pygame.SRCALPHA)
        self.popupsurface2.fill((0, 0, 0, 0))

        border_radius = 10
        popup_color2 = (self.darkBrown
                        )
        pygame.draw.rect(self.popupsurface2, popup_color2,
                         self.popupsurface2.get_rect(), border_radius=border_radius)
        self.popupsurfaceRect2 = self.popupsurface2.get_rect()
        self.popupsurfaceRect2.center = (
            (self.boardSizeX/2)+(self.screenSizeX - self.boardSizeX) //
            2, (self.boardSizeY/2)+self.wallSize//1.5+6)

        # BACK SURFACE
        self.backRect = pygame.Rect(
            517, 500, 80, 80/2)
        self.backSurface = pygame.Surface((80, 80/2))
        bordernext = pygame.Surface((80, 5+80/2))

        self.backSurface.fill(self.Red)
        bordernext.fill(self.darkRed)

        self.backSurfaceRect = self.backSurface.get_rect()
        self.backSurfaceRect.center = (
            self.popupsurfaceX//3, (self.popupsurfaceY//12)*11)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        backMessage = fontOk.render('Back', True, self.whiteSmoke)
        backMessage_rect = backMessage.get_rect()
        backMessage_rect.center = ((80//2, (80/2)//2))
        self.backSurface.blit(backMessage, backMessage_rect)
        self.popupsurface.blit(
            bordernext,
            self.backSurfaceRect)
        self.popupsurface.blit(self.backSurface,  self.backSurfaceRect)

        # launchParty SURFACE
        self.launchPartyRect = pygame.Rect(
            680, 500, 80, 80/2)
        self.launchPartySurface = pygame.Surface((80, 80/2))
        borderlaunchParty = pygame.Surface((80, 5+80/2))

        self.launchPartySurface.fill(self.green)
        borderlaunchParty.fill(self.darkGreen)

        self.launchPartySurfaceRect = self.launchPartySurface.get_rect()
        self.launchPartySurfaceRect.center = (
            (self.popupsurfaceX//3)*2, (self.popupsurfaceY//12)*11)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 20)
        launchPartyMessage = fontOk.render(
            'Start', True, self.whiteSmoke)
        launchPartyMessage_rect = launchPartyMessage.get_rect()
        launchPartyMessage_rect.center = ((80//2, (80/2)//2))
        self.launchPartySurface.blit(
            launchPartyMessage, launchPartyMessage_rect)
        self.popupsurface.blit(
            borderlaunchParty, self.launchPartySurfaceRect)
        self.popupsurface.blit(self.launchPartySurface,
                               self.launchPartySurfaceRect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # RULES SURFACE
        self.rulesButtonX = 350
        self.rulesButtonY = 50

        self.rulesSurface = pygame.Surface(
            (self.rulesButtonX, self.rulesButtonY))
        borderrules = pygame.Surface((self.rulesButtonX, 5+self.rulesButtonY))

        self.rulesSurface.fill(self.black)
        borderrules.fill(self.black2)

        self.rulesSurfaceRect = self.rulesSurface.get_rect()
        self.rulesSurfaceRect.center = (
            (self.popupsurfaceX//2), (self.popupsurfaceY//8))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        rulesMessage = fontOk.render('Human Players', True, self.whiteSmoke)
        rulesMessage_rect = rulesMessage.get_rect()
        rulesMessage_rect.center = (
            (self.rulesButtonX//2, (self.rulesButtonY)//2))
        self.rulesSurface.blit(rulesMessage, rulesMessage_rect)
        self.popupsurface.blit(
            borderrules, self.rulesSurfaceRect)
        self.popupsurface.blit(self.rulesSurface,  self.rulesSurfaceRect)

        # Player number5 SURFACE
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.oneHumanRect = pygame.Rect(
            417, 211, self.playerNbButtonX, self.playerNbButtonY)
        self.playerNbSurface5 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer5Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalHuman == 1:
            self.playerNbSurface5.fill(self.blue)
            borderplayer5Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface5.fill(self.beige3)
            borderplayer5Nb.fill(self.gray3)

        self.playerNbSurface5Rect = self.playerNbSurface5.get_rect()
        self.playerNbSurface5Rect.center = (
            (self.popupsurfaceX//8), (self.popupsurfaceY//8)*3-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('1', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface5.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer5Nb, self.playerNbSurface5Rect)
        self.popupsurface.blit(self.playerNbSurface5,
                               self.playerNbSurface5Rect)

        # Player number 7 Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.twoHumanRect = pygame.Rect(
            540, 211, self.playerNbButtonX, self.playerNbButtonY)
        self.playerNbSurface7 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer7Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalHuman == 2:
            self.playerNbSurface7.fill(self.blue)
            borderplayer7Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface7.fill(self.beige3)
            borderplayer7Nb.fill(self.gray3)

        self.playerNbSurface7Rect = self.playerNbSurface7.get_rect()
        self.playerNbSurface7Rect.center = (
            (self.popupsurfaceX//8)*3, ((self.popupsurfaceY//8)*3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('2', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface7.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer7Nb, self.playerNbSurface7Rect)
        self.popupsurface.blit(self.playerNbSurface7,
                               self.playerNbSurface7Rect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)

        # Player number9 SURFACE
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.threeHumanRect = pygame.Rect(
            664, 211, self.playerNbButtonX, self.playerNbButtonY)
        self.threeHuman = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer9Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalHuman == 3:
            self.playerNbSurface9.fill(self.blue)
            borderplayer9Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface9.fill(self.beige3)
            borderplayer9Nb.fill(self.gray3)

        self.playerNbSurface9Rect = self.playerNbSurface9.get_rect()
        self.playerNbSurface9Rect.center = (
            (self.popupsurfaceX//8)*5, ((self.popupsurfaceY//8)*3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('3', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface9.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer9Nb, self.playerNbSurface9Rect)
        self.popupsurface.blit(self.playerNbSurface9,
                               self.playerNbSurface9Rect)

        # Player number 11 Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.fourHumanRect = pygame.Rect(
            789, 211, self.playerNbButtonX, self.playerNbButtonY)
        self.playerNbSurface11 = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer11Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalHuman == 4:
            self.playerNbSurface11.fill(self.blue)
            borderplayer11Nb.fill(self.darkBlue)
        else:
            self.playerNbSurface11.fill(self.beige3)
            borderplayer11Nb.fill(self.gray3)

        self.playerNbSurface11Rect = self.playerNbSurface11.get_rect()
        self.playerNbSurface11Rect.center = (
            (self.popupsurfaceX//8)*7, ((self.popupsurfaceY//8)*3)-20)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('4', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.playerNbSurface11.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer11Nb, self.playerNbSurface11Rect)
        self.popupsurface.blit(self.playerNbSurface11,
                               self.playerNbSurface11Rect)

        # Wall number SURFACE
        self.rulesButtonX = 350
        self.rulesButtonY = 50

        self.rulesSurface = pygame.Surface(
            (self.rulesButtonX, self.rulesButtonY))
        borderrules = pygame.Surface((self.rulesButtonX, 5+self.rulesButtonY))

        self.rulesSurface.fill(self.black)
        borderrules.fill(self.black2)

        self.rulesSurfaceRect = self.rulesSurface.get_rect()
        self.rulesSurfaceRect.center = (
            (self.popupsurfaceX//2), ((self.popupsurfaceY//8)*4)+12)
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        rulesMessage = fontOk.render('Bot Players', True, self.whiteSmoke)
        rulesMessage_rect = rulesMessage.get_rect()
        rulesMessage_rect.center = (
            (self.rulesButtonX//2, (self.rulesButtonY)//2))
        self.rulesSurface.blit(rulesMessage, rulesMessage_rect)
        self.popupsurface.blit(
            borderrules, self.rulesSurfaceRect)
        self.popupsurface.blit(self.rulesSurface,  self.rulesSurfaceRect)

        # Player number5 SURFACE
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.zeroBotRect = pygame.Rect(
            417, 394, self.playerNbButtonX, self.playerNbButtonY)
        self.zeroBot = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer5Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalBot == 0:
            self.zeroBot.fill(self.blue)
            borderplayer5Nb.fill(self.darkBlue)
        else:
            self.zeroBot.fill(self.beige3)
            borderplayer5Nb.fill(self.gray3)

        self.playerNbSurface5Rect = self.zeroBot.get_rect()
        self.playerNbSurface5Rect.center = (
            (self.popupsurfaceX//8), ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('0', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.zeroBot.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer5Nb, self.playerNbSurface5Rect)
        self.popupsurface.blit(self.zeroBot,
                               self.playerNbSurface5Rect)

        # Player number 7 Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.oneBotRect = pygame.Rect(
            541, 394, self.playerNbButtonX, self.playerNbButtonY)
        self.oneBot = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer9Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalBot == 1:
            self.oneBot.fill(self.blue)
            borderplayer9Nb.fill(self.darkBlue)
        else:
            self.oneBot.fill(self.beige3)
            borderplayer9Nb.fill(self.gray3)

        self.playerNbSurface9Rect = self.oneBot.get_rect()
        self.playerNbSurface9Rect.center = (
            (self.popupsurfaceX//8)*3, ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('1', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.oneBot.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer9Nb, self.playerNbSurface9Rect)
        self.popupsurface.blit(self.oneBot,
                               self.playerNbSurface9Rect)

        # Player number9 SURFACE
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.twoBotRect = pygame.Rect(
            665, 394, self.playerNbButtonX, self.playerNbButtonY)
        self.twoBot = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer9Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalBot == 2:
            self.twoBot.fill(self.blue)
            borderplayer9Nb.fill(self.darkBlue)
        else:
            self.twoBot.fill(self.beige3)
            borderplayer9Nb.fill(self.gray3)

        self.playerNbSurface9Rect = self.twoBot.get_rect()
        self.playerNbSurface9Rect.center = (
            (self.popupsurfaceX//8)*5, ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('2', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.twoBot.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer9Nb, self.playerNbSurface9Rect)
        self.popupsurface.blit(self.twoBot,
                               self.playerNbSurface9Rect)

        # Player number 11 Surface
        self.playerNbButtonX = 70
        self.playerNbButtonY = 65
        self.threeBotRect = pygame.Rect(
            789, 394, self.playerNbButtonX, self.playerNbButtonY)
        self.threeBot = pygame.Surface(
            (self.playerNbButtonX, self.playerNbButtonY))
        borderplayer11Nb = pygame.Surface(
            (self.playerNbButtonX, 5+self.playerNbButtonY))

        if self.totalBot == 3:
            self.threeBot.fill(self.blue)
            borderplayer11Nb.fill(self.darkBlue)
        else:
            self.threeBot.fill(self.beige3)
            borderplayer11Nb.fill(self.gray3)

        self.playerNbSurface11Rect = self.threeBot.get_rect()
        self.playerNbSurface11Rect.center = (
            (self.popupsurfaceX//8)*7, ((self.popupsurfaceY//8)*6-12))
        fontOk = pygame.font.Font("assets/font/chalk_scratch.otf", 30)
        playerNbMessage = fontOk.render('3', True, self.black)
        playerNbMessage_rect = playerNbMessage.get_rect()
        playerNbMessage_rect.center = (
            (self.playerNbButtonX//2, (self.playerNbButtonY)//2))

        self.threeBot.blit(playerNbMessage, playerNbMessage_rect)
        self.popupsurface.blit(
            borderplayer11Nb, self.playerNbSurface11Rect)
        self.popupsurface.blit(self.threeBot,
                               self.playerNbSurface11Rect)

        self.screen.blit(self.popupsurface2, self.popupsurfaceRect2)
        self.screen.blit(self.popupsurface, self.popupsurfaceRect)
        pygame.display.update()

    def runMenu(self):
        while self.menuRunning:
            self.handlingMenuEvent()
            self.displayMenus()
            pygame.display.flip()
        self.menuRunning = False

    def majVariables(self):

        if self.nbPlayers >= 3:
            self.player3 = True
        if self.nbPlayers == 4:
            self.player4 = True

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

        self.cell = pygame.Surface(
            (self.cellSize, self.cellSize))
        self.pannelSizeX = self.cellSize*self.fakeGridSize + \
            self.wallSize*(self.fakeGridSize-1)
        self.pannelPositionY = self.cellSize+self.wallSize+self.cellSize * \
            self.fakeGridSize+self.wallSize * \
            (self.fakeGridSize-1)+self.wallSize//2

        # définition de surafaces pour le hover des cellules et murs
        self.cellHover = pygame.Surface(
            (self.cellSize, self.cellSize))
        self.cellHoverBorder = pygame.Surface(
            (self.cellSize, self.wallSize//2))
        self.verticalWallHover = pygame.Surface(
            (self.wallSize, self.cellSize*2+self.wallSize))
        self.horizontalWallHover = pygame.Surface(
            (self.cellSize*2+self.wallSize, self.wallSize))

        # définition des surfaces de clique pour les in-game menu
        self.exitRect = pygame.Rect(
            330, 0, self.cellSize, self.cellSize)
        self.settingsRect = pygame.Rect(
            self.settingX, 0, self.cellSize, self.cellSize)

        # Création d'un dictionnire pour stocker les informations sur chaque joueur

        self.infosPlayers = {}
        for i in range(1, self.totalHuman + 1):
            self.infosPlayers[f'player {i}'] = {
                'nature': 'human'}
        for i in range(self.totalHuman + 1, self.nbPlayers + 1):
            self.infosPlayers[f'player {i}'] = {
                'nature': 'bot'}

        # cette boucle va attribuer une nature aux cases
        self.grid = [[case() for i in range(30)]
                     for j in range(30)]
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
                        # barrières "parasites"
                        self.grid[i][j].setNature(7)

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
                        # barrières "parasites"
                        self.grid[i][j].setNature(7)

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
                        self.grid[i][j].setNature(
                            7)  # barrières "parasites

        self.player1barriers = self.nbBarrierPerPlayer
        self.player2barriers = self.nbBarrierPerPlayer
        self.player3barriers = self.nbBarrierPerPlayer
        self.player4Barriers = self.nbBarrierPerPlayer

    def startServer(self):
        # Pass the current Jeu instance (self) to the Server

        print("cuurentplayer choice = ", self.currentPlayer)
        self.server = Server(self, self.player1barriers, self.player2barriers, self.player3barriers, self.player4Barriers, self.currentPlayer,
                             self.player_id, self.gridSize, self.nbBarrierPerPlayer, self.totalBot, self.totalHuman, self.nbPlayers, self.fakeGridSize)
        self.server.start()

    def client(self):
        host, port = ("localhost", 5566)
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            my_socket.connect((host, port))
            print("client connecté !")

        except:
            print("connexion au serveur échoué !")

        # initialisation des choix faits par le serveur
        def initVar():
            # serialized_game = my_socket.recv(16384)
            # self.grid = pickle.loads(serialized_game)

            serialized_data = my_socket.recv(16384)
            data = pickle.loads(serialized_data)

            self.player1barriers = int(data[0])
            self.player2barriers = int(data[1])
            self.player3barriers = int(data[2])
            self.player4Barriers = int(data[3])
            self.currentPlayer = int(data[4])
            self.player_id = int(data[5])
            self.gridSize = int(data[6])
            self.nbBarrierPerPlayer = int(data[7])
            self.totalBot = int(data[8])
            self.totalHuman = int(data[9])
            self.nbPlayers = int(data[10])
            self.fakeGridSize = int(data[11])
            self.majVariables()

            serialized_id = my_socket.recv(16384)
            self.player_id = pickle.loads(serialized_id)
            print("id", self.player_id)

            print("id =", self.player_id, "current player=", self.currentPlayer)

        # fonction permettant aux clients de jouer ou re9voir le plateau
        def play():

            self.drawCellHeight()
            while self.currentPlayer == self.player_id:

                # attente d'action du joueur qui doit jouer
                self.handlingGameEvents()
                self.displayScreen()
                self.drawPlayerDirection()
                self.displayHover()
                if self.ShowSettingsMenu == True:
                    self.displaySettingsMenu()
                pygame.display.flip()
                print("current player", self.currentPlayer)
                self.clock.tick(30)

                # envoie des données au serveurs
                # print("data sent to server by player after a play (im player) ",data)
                # serialized_game = pickle.dumps(self.grid)
                # my_socket.sendall(serialized_game)

                # data = [str(self.player1barriers), str(self.player2barriers), str(
                #     self.player3barriers), str(self.player4Barriers), str(self.currentPlayer)]

                # serialized_data = pickle.dumps(data)
                # my_socket.sendall(serialized_data)

            while True:

                # affichage plateau
                self.handlingGameEvents()
                self.displayScreen()
                pygame.display.flip()
                self.clock.tick(30)
                print("current player", self.currentPlayer)
                # reception données
                # print("data received  from server after a play (im client)")
                # my_socket.setblocking(0)
                # serialized_game = my_socket.recv(16384)
                # self.grid = pickle.loads(serialized_game)

                # serialized_data = my_socket.recv(16384)
                # data = pickle.loads(serialized_data)

                # # mise a jour données
                # self.player1barriers = int(data[0])
                # self.player2barriers = int(data[1])
                # self.player3barriers = int(data[2])
                # self.player4Barriers = int(data[3])
                # self.currentPlayer = int(data[4])
        try:
            initVar()
            play()

        except (EOFError):
            print("Error: Connection to server lost.")
            my_socket.close()


class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket, server, jeu, data, num_clients):
        threading.Thread.__init__(self)
        self.client_address = client_address
        self.client_socket = client_socket
        self.server = server
        self.jeu = jeu
        self.data = data
        self.num_clients = num_clients

    def init_host_choices(self):
        serialized_data = pickle.dumps(self.data)
        self.client_socket.sendall(serialized_data)

        serialized_id = pickle.dumps(self.num_clients)
        self.client_socket.sendall(serialized_id)

    def run(self):
        print("client connecté !")
        self.init_host_choices()
        # while True:

        # serialized_game = self.client_socket.recv(16384)
        # self.grid = pickle.loads(serialized_game)

        # serialized_data = self.client_socket.recv(16384)
        # data = pickle.loads(serialized_data)

        # serialized_game = pickle.dumps(self.grid)
        # self.client_socket.sendall(serialized_game)

        # serialized_data = pickle.dumps(self.data)
        # self.client_socket.sendall(serialized_data)


class Server:
    def __init__(self, jeu, player1barriers, player2barriers, player3barriers, player4Barriers, currentPlayer, player_id, gridSize, nbBarrierPerPlayer, totalBot, totalHuman, nbPlayers, fakeGridSize):
        self.threads = []
        self.sockets = []
        self.jeu = jeu
        self.data = [str(player1barriers), str(player2barriers), str(player3barriers), str(player4Barriers), str(currentPlayer), str(
            player_id), str(gridSize), str(nbBarrierPerPlayer), str(totalBot), str(totalHuman), str(nbPlayers), str(fakeGridSize)]

    def start(self):
        server_socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 5566))
        print("le serveur est lancé...")

        num_clients = 0
        while num_clients < 3:
            server_socket.listen(1)
            client_socket, client_address = server_socket.accept()
            self.sockets.append(client_socket)
            num_clients += 1
            new_thread = ClientThread(
                client_address, client_socket, self, self.jeu, self.data, num_clients)
            new_thread.init_host_choices()
            new_thread.start()
            self.threads.append(new_thread)
    # ...


if __name__ == "__main__":
    pygame.init()
    game = jeu()
    game.runMenu()
    # nnnnnnnnnnnn
