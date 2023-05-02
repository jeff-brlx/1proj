import curses
from termcolor import colored
import copy


class case:
    def __init__(self):
        self.nature = 70
    # regarde la nature des cases (chemin,pion,barrière réelle, barrière parasite)

    def checkNature(self):
        #  et les affiche
        if self.nature == 0:
            return "\u25A0"
        if self.nature == 1:
            return " "  # barrières "-" NON VISIBLES
        if self.nature == 2:
            return " "  # barrières "|" NON VISIBLES
        if self.nature == 10:
            return colored("\u25A0", "red")  # barrières "-" VISIBLES
        if self.nature == 20:
            return colored("\u25A0", "red")  # barrières "|" VISIBLES

        if self.nature == 4:
            return colored("\u25A0", "blue")  # pion joueur 1
        if self.nature == 5:
            return colored("\u25A0", "green")  # pion joueur 2

        if self.nature == 6:
            return colored("\u25A0", "yellow")  # pion joueur 3
        if self.nature == 8:
            return colored("\u25A0", "magenta")  # pion joueur 4

        if self.nature == 7:
            return " "  # barrières parasites

    def getNature(self):
        return self.nature

    def setNature(self, newNature):
        self.nature = newNature


class jeu:

    def __init__(self):
        self.nbPlayers = None
        while self.nbPlayers not in [2, 3, 4]:
            try:
                self.nbPlayers = int(
                    input("Enter the number of players: "))
                if self.nbPlayers not in [2, 3, 4]:
                    print("Invalid input. Please enter a number between 2 and 4.")
            except ValueError:
                print("Invalid input. Please enter a number between 2 and 4.")

        self.gridSize = None
        while self.gridSize not in [5, 7, 9, 11]:
            try:
                self.gridSize = int(input("Enter a grid Size: "))
                if self.gridSize not in [5, 7, 9, 11]:
                    print(
                        "Invalid input. Please enter a number equal to : 5 , 7 , 9 or 11.")
            except ValueError:
                print(
                    "Invalid input. Please enter a number equal to : 5 , 7 , 9 or 11. ")

        # calcul permettant de créer une grille avec la bonne taille
        self.gridSize = self.gridSize*2-1
        # (les indices des barrières ne sont pas comptées)
        self.currentPlayer = 1

        self.grid = [[case() for i in range(self.gridSize)]
                     for j in range(self.gridSize)]

        # cette boucle va attribuer une nature aux cases en fonction
        for i in range(self.gridSize):
            # de leur position dans le tableau (0 or 1 or 2 or 4 or 5 or 7)
            for j in range(self.gridSize):

                if self.nbPlayers == 2:
                    if i == 0 and j == (self.gridSize//2):
                        # initialise le pions du joueur 1 (millieu 1ère ligne)
                        self.grid[i][j].setNature(4)

                    elif (i == self.gridSize-1 and j == self.gridSize//2):
                        # initialise le pions du joueur 2 (millieu 2ème ligne)
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
                        self.grid[i][j].setNature(7)  # barrières "parasites"

    def getCurrentPlayer(self):
        return self.currentPlayer

    def getGrid(self):
        return self.grid

    def setGrid(self, gridCopy):
        self.grid = gridCopy

    def displayGrid(self):  # affiche un tableau d'objet case

        for i in range(self.gridSize):
            for j in range(self.gridSize):
                # Recupere la nature des cases puis les affiches en fonction
                print(self.grid[i][j].checkNature(), end=" ")
            print()

    def movePawn(self):  # déplacement des pions
        # on stock la grille pour vérifier à la fin si elle a changé . si ce n'est pas le cas le mouvment est donc invalid
        self.gridCopy = self.grid
        if self.currentPlayer == 1:
            move = input(
                "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            while move not in ["u", "d", "l", "r"]:
                print("incorrect choice , try again")
                move = input(
                    "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            if move == "d":  # Descendre
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if i < self.gridSize - 1 and self.grid[i][j].getNature() == 4 and (self.grid[i+2][j].getNature() == 5 or self.grid[i+2][j].getNature() == 6 or self.grid[i+2][j].getNature() == 8) and ((i+3 < self.gridSize-1 and self.grid[i+3][j].getNature() == 10) or i+2 == self.gridSize-1):
                            choice = str(
                                input("down Left ( dl ) or down Right ( dr ) :").lower())
                            while choice not in ["dl", "dr"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("down Left ( dl ) or down Right ( dr ) :").lower())
                            if choice == "dl" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "dr" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 4 and i+2 < self.gridSize and self.grid[i+1][j].getNature() != 10:

                            if self.grid[i+2][j].getNature() != 5 and self.grid[i+2][j].getNature() != 6 and self.grid[i+2][j].getNature() != 8:
                                self.grid[i+2][j].setNature(4)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if (self.grid[i+4][j].getNature() == 0):
                                    self.grid[i+4][j].setNature(4)
                                    self.grid[i][j].setNature(0)
                                return

            elif move == "u":  # Monter
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 4 and (self.grid[i-2][j].getNature() == 5 or self.grid[i-2][j].getNature() == 6 or self.grid[i-2][j].getNature() == 8) and ((i-3 > 0 and self.grid[i-3][j].getNature() == 10) or i-2 == 0):
                            choice = str(
                                input("up Left ( ul ) or up Right ( ur ) :").lower())
                            while choice not in ["ul", "ur"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("up Left ( ul ) or up Right ( ur ):").lower())
                            if choice == "ul" and self.grid[i-2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ur" and self.grid[i-2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 4 and i-2 >= 0 and self.grid[i-1][j].getNature() != 10:

                            if self.grid[i-2][j].getNature() != 5 and self.grid[i-2][j].getNature() != 6 and self.grid[i-2][j].getNature() != 8:
                                self.grid[i-2][j].setNature(4)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if (self.grid[i-4][j].getNature() == 0):
                                    self.grid[i-4][j].setNature(4)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "r":  # Droite
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if j < self.gridSize - 1 and self.grid[i][j].getNature() == 4 and (self.grid[i][j+2].getNature() == 5 or self.grid[i][j+2].getNature() == 6 or self.grid[i][j+2].getNature() == 8) and ((j+3 < self.gridSize-1 and self.grid[i][j+3].getNature() == 20) or j+2 == self.gridSize-1):
                            choice = str(
                                input("right up ( ru ) or right down ( rd ):").lower())
                            while choice not in ["ru", "rd"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("right up ( ru ) or right down ( rd ):").lower())
                            if choice == "ru" and self.grid[i-2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "rd" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 4 and j+2 < self.gridSize and self.grid[i][j+1].getNature() != 20:

                            if self.grid[i][j+2].getNature() != 5 and self.grid[i][j+2].getNature() != 6 and self.grid[i][j+2].getNature() != 8:
                                self.grid[i][j+2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if (self.grid[i][j+4].getNature() == 0):
                                    self.grid[i][j+4].setNature(4)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "l":  # Gauche
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 4 and (self.grid[i][j-2].getNature() == 5 or self.grid[i][j-2].getNature() == 6 or self.grid[i][j-2].getNature() == 8) and ((j-3 > 0 and self.grid[i][j-3].getNature() == 20) or j-2 == self.gridSize-1):
                            choice = str(
                                input("Left up ( lu ) or left down ( ld ) :").lower())
                            while choice not in ["lu", "ld"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("Left up ( lu ) or left down ( ld ) :").lower())
                            if choice == "lu" and self.grid[i-2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ld" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 4 and j-2 >= 0 and self.grid[i][j-1].getNature() != 20:

                            if self.grid[i][j-2].getNature() != 5 and self.grid[i][j-2].getNature() != 6 and self.grid[i][j-2].getNature() != 8:
                                self.grid[i][j-2].setNature(4)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if (self.grid[i][j-4].getNature() == 0):
                                    self.grid[i][j-4].setNature(4)
                                    self.grid[i][j].setNature(0)
                                    return

        if self.currentPlayer == 2:
            move = input(
                "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            while move not in ["u", "d", "l", "r"]:
                print("incorrect choice , try again")
                move = input(
                    "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            if move == "d":  # Descendre
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if i < self.gridSize - 1 and self.grid[i][j].getNature() == 5 and (self.grid[i+2][j].getNature() == 4 or self.grid[i+2][j].getNature() == 6 or self.grid[i+2][j].getNature() == 8) and ((i+3 < self.gridSize-1 and self.grid[i+3][j].getNature() == 10) or i+2 == self.gridSize-1):
                            choice = str(
                                input("down Left ( dl ) or down Right ( dr ) :").lower())
                            while choice not in ["dl", "dr"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("down Left ( dl ) or down Right ( dr ) :").lower())
                            if choice == "dl" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "dr" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 5 and i+2 < self.gridSize and self.grid[i+1][j].getNature() != 10:

                            if self.grid[i+2][j].getNature() != 4 and self.grid[i+2][j].getNature() != 6 and self.grid[i+2][j].getNature() != 8:
                                self.grid[i+2][j].setNature(5)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i+4][j].getNature() == 0:
                                    self.grid[i+4][j].setNature(5)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "u":  # Monter
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 5 and (self.grid[i-2][j].getNature() == 4 or self.grid[i-2][j].getNature() == 6 or self.grid[i-2][j].getNature() == 8) and ((i-3 > 0 and self.grid[i-3][j].getNature() == 10) or i-2 == 0):
                            choice = str(
                                input("up Left ( ul ) or up Right ( ur ) :").lower())
                            while choice not in ["ul", "ur"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("up Left ( ul ) or up Right ( ur ):").lower())
                            if choice == "ul" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ur" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 5 and i-2 >= 0 and self.grid[i-1][j].getNature() != 10:

                            if self.grid[i-2][j].getNature() != 4 and self.grid[i-2][j].getNature() != 6 and self.grid[i-2][j].getNature() != 8:
                                self.grid[i-2][j].setNature(5)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i-4][j].getNature() == 0:
                                    self.grid[i-4][j].setNature(5)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "r":  # Droite
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if j < self.gridSize - 1 and self.grid[i][j].getNature() == 5 and (self.grid[i][j+2].getNature() == 4 or self.grid[i][j+2].getNature() == 6 or self.grid[i][j+2].getNature() == 8) and ((j+3 < self.gridSize-1 and self.grid[i][j+3].getNature() == 20) or j+2 == self.gridSize-1):
                            choice = str(
                                input("right up ( ru ) or right down ( rd ):").lower())
                            while choice not in ["ru", "rd"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("right up ( ru ) or right down ( rd ):").lower())
                            if choice == "ru" and self.grid[i-2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "rd" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return
                        elif self.grid[i][j].getNature() == 5 and j+2 < self.gridSize and self.grid[i][j+1].getNature() != 20:
                            # saut de deux indices
                            if self.grid[i][j+2].getNature() != 4 and self.grid[i][j+2].getNature() != 6 and self.grid[i][j+2].getNature() != 8:
                                self.grid[i][j+2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i][j+4].getNature() == 0:
                                    self.grid[i][j+4].setNature(5)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "l":  # Gauche
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 5 and (self.grid[i][j-2].getNature() == 4 or self.grid[i][j-2].getNature() == 6 or self.grid[i][j-2].getNature() == 8) and ((j-3 > 0 and self.grid[i][j-3].getNature() == 20) or j-2 == self.gridSize-1):
                            choice = str(
                                input("Left up ( lu ) or left down ( ld ) :").lower())
                            while choice not in ["lu", "ld"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("Left up ( lu ) or left down ( ld ) :").lower())
                            if choice == "lu" and self.grid[i-2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ld" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return
                        elif self.grid[i][j].getNature() == 5 and j-2 >= 0 and self.grid[i][j-1].getNature() != 20:

                            if self.grid[i][j-2].getNature() != 4 and self.grid[i][j-2].getNature() != 6 and self.grid[i][j-2].getNature() != 8:
                                self.grid[i][j-2].setNature(5)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i][j-4].getNature() == 0:
                                    self.grid[i][j-4].setNature(5)
                                    self.grid[i][j].setNature(0)
                                    return

        if self.currentPlayer == 3:
            move = input(
                "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            while move not in ["u", "d", "l", "r"]:
                print("incorrect choice , try again")
                move = input(
                    "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            if move == "d":  # Descendre
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if i < self.gridSize - 1 and self.grid[i][j].getNature() == 6 and (self.grid[i+2][j].getNature() == 4 or self.grid[i+2][j].getNature() == 5 or self.grid[i+2][j].getNature() == 8) and ((i+3 < self.gridSize-1 and self.grid[i+3][j].getNature() == 10) or i+2 == self.gridSize-1):
                            choice = str(
                                input("down Left ( dl ) or down Right ( dr ) :").lower())
                            while choice not in ["dl", "dr"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("down Left ( dl ) or down Right ( dr ) :").lower())

                            if choice == "dl" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "dr" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 6 and i+2 < self.gridSize and self.grid[i+1][j].getNature() != 10:

                            if self.grid[i+2][j].getNature() != 4 and self.grid[i+2][j].getNature() != 5 and self.grid[i+2][j].getNature() != 8:
                                self.grid[i+2][j].setNature(6)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i+4][j].getNature() == 0:
                                    self.grid[i+4][j].setNature(6)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "u":  # Monter
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 6 and (self.grid[i-2][j].getNature() == 4 or self.grid[i-2][j].getNature() == 5 or self.grid[i-2][j].getNature() == 8) and ((i-3 > 0 and self.grid[i-3][j].getNature() == 10) or i-2 == 0):
                            choice = str(
                                input("up Left ( ul ) or up Right ( ur ) :").lower())
                            while choice not in ["ul", "ur"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("up Left ( ul ) or up Right ( ur ):").lower())
                            if choice == "ul" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ur" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 6 and i-2 >= 0 and self.grid[i-1][j].getNature() != 10:

                            if self.grid[i-2][j].getNature() != 4 and self.grid[i-2][j].getNature() != 5 and self.grid[i-2][j].getNature() != 8:
                                self.grid[i-2][j].setNature(6)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i-4][j].getNature() == 0:
                                    self.grid[i-4][j].setNature(6)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "r":  # Droite
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if j < self.gridSize - 1 and self.grid[i][j].getNature() == 6 and (self.grid[i][j+2].getNature() == 4 or self.grid[i][j+2].getNature() == 5 or self.grid[i][j+2].getNature() == 8) and ((j+3 < self.gridSize-1 and self.grid[i][j+3].getNature() == 20) or j+2 == self.gridSize-1):
                            choice = str(
                                input("right up ( ru ) or right down ( rd ):").lower())
                            while choice not in ["ru", "rd"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("right up ( ru ) or right down ( rd ):").lower())
                            if choice == "ru" and self.grid[i-2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "rd" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return
                        elif self.grid[i][j].getNature() == 6 and j+2 < self.gridSize and self.grid[i][j+1].getNature() != 20:
                            # saut de deux indices
                            if self.grid[i][j+2].getNature() != 4 and self.grid[i][j+2].getNature() != 5 and self.grid[i][j+2].getNature() != 8:
                                self.grid[i][j+2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i][j+4].getNature() == 0:
                                    self.grid[i][j+4].setNature(6)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "l":  # Gauche
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 6 and (self.grid[i][j-2].getNature() == 4 or self.grid[i][j-2].getNature() == 5 or self.grid[i][j-2].getNature() == 8) and ((j-3 > 0 and self.grid[i][j-3].getNature() == 20) or j-2 == self.gridSize-1):
                            choice = str(
                                input("Left up ( lu ) or left down ( ld ) :").lower())
                            while choice not in ["lu", "ld"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("Left up ( lu ) or left down ( ld ) :").lower())
                            if choice == "lu" and self.grid[i-2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ld" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return
                        elif self.grid[i][j].getNature() == 6 and j-2 >= 0 and self.grid[i][j-1].getNature() != 20:

                            if self.grid[i][j-2].getNature() != 4 and self.grid[i][j-2].getNature() != 5 and self.grid[i][j-2].getNature() != 8:
                                self.grid[i][j-2].setNature(6)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i][j-4].getNature() == 0:
                                    self.grid[i][j-4].setNature(6)
                                    self.grid[i][j].setNature(0)
                                    return

        if self.currentPlayer == 4:
            move = input(
                "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            while move not in ["u", "d", "l", "r"]:
                print("incorrect choice , try again")
                move = input(
                    "up ( u ) , down ( d ) , left ( l ) , right ( r ): ").lower()
            if move == "d":  # Descendre
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if i < self.gridSize - 1 and self.grid[i][j].getNature() == 8 and (self.grid[i+2][j].getNature() == 4 or self.grid[i+2][j].getNature() == 5 or self.grid[i+2][j].getNature() == 6) and ((i+3 < self.gridSize-1 and self.grid[i+3][j].getNature() == 10) or i+2 == self.gridSize-1):
                            choice = str(
                                input("down Left ( dl ) or down Right ( dr ) :").lower())
                            while choice not in ["dl", "dr"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("down Left ( dl ) or down Right ( dr ) :").lower())
                            if choice == "dl" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "dr" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 8 and i+2 < self.gridSize and self.grid[i+1][j].getNature() != 10:

                            if self.grid[i+2][j].getNature() != 4 and self.grid[i+2][j].getNature() != 5 and self.grid[i+2][j].getNature() != 6:
                                self.grid[i+2][j].setNature(8)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i+4][j].getNature() == 0:
                                    self.grid[i+4][j].setNature(8)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "u":  # Monter
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 8 and (self.grid[i-2][j].getNature() == 4 or self.grid[i-2][j].getNature() == 5 or self.grid[i-2][j].getNature() == 6) and ((i-3 > 0 and self.grid[i-3][j].getNature() == 10) or i-2 == 0):
                            choice = str(
                                input("up Left ( ul ) or up Right ( ur ) :").lower())
                            while choice not in ["ul", "ur"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("up Left ( ul ) or up Right ( ur ):").lower())
                            if choice == "ul" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ur" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return

                        elif self.grid[i][j].getNature() == 8 and i-2 >= 0 and self.grid[i-1][j].getNature() != 10:

                            if self.grid[i-2][j].getNature() != 4 and self.grid[i-2][j].getNature() != 5 and self.grid[i-2][j].getNature() != 6:
                                self.grid[i-2][j].setNature(8)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i-4][j].getNature() == 0:
                                    self.grid[i-4][j].setNature(8)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "r":  # Droite
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if j < self.gridSize - 1 and self.grid[i][j].getNature() == 8 and (self.grid[i][j+2].getNature() == 4 or self.grid[i][j+2].getNature() == 5 or self.grid[i][j+2].getNature() == 6) and ((j+3 < self.gridSize-1 and self.grid[i][j+3].getNature() == 20) or j+2 == self.gridSize-1):
                            choice = str(
                                input("right up ( ru ) or right down ( rd ):").lower())
                            while choice not in ["ru", "rd"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("right up ( ru ) or right down ( rd ):").lower())
                            if choice == "ru" and self.grid[i-2][j+2].getNature() == 0:
                                self.grid[i-2][j+2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "rd" and self.grid[i+2][j+2].getNature() == 0:
                                self.grid[i+2][j+2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return
                        elif self.grid[i][j].getNature() == 8 and j+2 < self.gridSize and self.grid[i][j+1].getNature() != 20:
                            # saut de deux indices
                            if self.grid[i][j+2].getNature() != 4 and self.grid[i][j+2].getNature() != 5 and self.grid[i][j+2].getNature() != 6:
                                self.grid[i][j+2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i][j+4].getNature() == 0:
                                    self.grid[i][j+4].setNature(8)
                                    self.grid[i][j].setNature(0)
                                    return

            elif move == "l":  # Gauche
                for i in range(self.gridSize):
                    for j in range(self.gridSize):

                        if self.grid[i][j].getNature() == 8 and (self.grid[i][j-2].getNature() == 4 or self.grid[i][j-2].getNature() == 5 or self.grid[i][j-2].getNature() == 6) and ((j-3 > 0 and self.grid[i][j-3].getNature() == 20) or j-2 == self.gridSize-1):
                            choice = str(
                                input("Left up ( lu ) or left down ( ld ) :").lower())
                            while choice not in ["lu", "ld"]:
                                print("incorrect choice , try again")
                                choice = str(
                                    input("Left up ( lu ) or left down ( ld ) :").lower())
                            if choice == "lu" and self.grid[i-2][j-2].getNature() == 0:
                                self.grid[i-2][j-2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return

                            elif choice == "ld" and self.grid[i+2][j-2].getNature() == 0:
                                self.grid[i+2][j-2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return
                        elif self.grid[i][j].getNature() == 8 and j-2 >= 0 and self.grid[i][j-1].getNature() != 20:

                            if self.grid[i][j-2].getNature() != 4 and self.grid[i][j-2].getNature() != 5 and self.grid[i][j-2].getNature() != 6:
                                self.grid[i][j-2].setNature(8)
                                self.grid[i][j].setNature(0)
                                return
                            else:
                                if self.grid[i][j-4].getNature() == 0:
                                    self.grid[i][j-4].setNature(8)
                                    self.grid[i][j].setNature(0)
                                    return
        # la grille n'a pas changée => mouvement invalide
        while (self.grid == self.gridCopy):
            print("invalid move , try again")
            return self.movePawn()

    def placeWall(self):  # placement des murs
        gridCopy = copy.deepcopy(self.grid)
        x = None
        while x not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            try:
                x = int(
                    input("Enter an abscissa: "))
                if x not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    print("Invalid input. Please enter a number between 0 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 9.")

        y = None
        while y not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            try:
                y = int(
                    input("Enter an ordiante: "))
                if y not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
                    print("Invalid input. Please enter a number between 0 and 9.")
            except ValueError:
                print("Invalid input. Please enter a number between 0 and 9.")

        if (x+2 <= self.gridSize and y+2 <= self.gridSize):
            if self.grid[x][y].getNature() == 1 and self.grid[x][y+1].getNature() == 7 and self.grid[x][y+2].getNature() == 1:
                self.grid[x][y].setNature(10)
                self.grid[x][y+1].setNature(10)
                self.grid[x][y+2].setNature(10)

            elif self.grid[x][y].getNature() == 2 and self.grid[x+1][y].getNature() == 7 and self.grid[x+2][y].getNature() == 2:
                self.grid[x][y].setNature(20)
                self.grid[x+1][y].setNature(20)
                self.grid[x+2][y].setNature(20)
            else:
                print("invalid choice . Please try again ")
                return self.placeWall()

        # vérification des chemins

        if self.nbPlayers == 2:
            if self.pathFinding(4, self.grid) == False or self.pathFinding(5, self.grid) == False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = gridCopy
                # self.displayGrid()
                print("impossible to place this wall . Please try again")
                return self.placeWall()
            else:
                return

        elif self.nbPlayers == 3:
            if self.pathFinding(4, self.grid) == False or self.pathFinding(5, self.grid) == False or self.pathFinding(6, self.grid) == False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = gridCopy
                print("impossible to place this wall . Please try again")
                return self.placeWall()  # le joueur peut refaire un choix d'action

        elif self.nbPlayers == 4:
            if self.pathFinding(4, self.grid) == False or self.pathFinding(5, self.grid) == False or self.pathFinding(6, self.grid) == False or self.pathFinding(8, self.grid) == False:
                # la version précédente de la grille est restaurée si un pion est bloqué
                self.grid = gridCopy
                print("impossible to place this wall . Please try again")
                return self.placeWall()  # le joueur peut refaire un choix d'action

    def pathFinding(self, start, grid):
        # recherche du joueur sur la grille (start=joueur)
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
            if row < self.gridSize-2 and grid[row+1][col].getNature() != 10:
                neighbors.append((row+2, col))

            if row >= 0 and grid[row-1][col].getNature() != 10:
                neighbors.append((row-2, col))

            if col < self.gridSize-2 and grid[row][col+1].getNature() != 20:
                neighbors.append((row, col+2))

            if col >= 0 and grid[row][col-1].getNature() != 20:
                neighbors.append((row, col-2))

            for neighbor in neighbors:
                r, c = neighbor
                if 0 <= r < self.gridSize and 0 <= c < self.gridSize and neighbor not in visited:
                    queue.append(neighbor)
                    visited.add(neighbor)

        return False  # chemin non trouvé pour le joueur

    def checkWin(self):
        # après un mouvement current_player = current_player + 1 , donc le gaga$nant est currentPlayer - 1
        win = False
        for i in range(self.gridSize):
            for j in range(self.gridSize):
                if (self.grid[i][j].getNature() == 4 and i == self.gridSize-1) or (self.grid[i][j].getNature() == 5 and i == 0) or (self.grid[i][j].getNature() == 8 and j == 0) or (self.grid[i][j].getNature() == 6 and j == self.gridSize-1):
                    win = True
                    break
        return win

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

    def nextPlayer(self):
        if self.nbPlayers > self.currentPlayer:
            self.currentPlayer += 1
        else:
            self.currentPlayer = 1

    def displayPlayerTurn(self):
        if self.currentPlayer == 1:
            print("player turn :", colored(self.currentPlayer, "blue"))
        elif self.currentPlayer == 2:
            print("player turn :", colored(self.currentPlayer, "green"))
        elif self.currentPlayer == 3:
            print("player turn :", colored(self.currentPlayer, "yellow"))
        elif self.currentPlayer == 4:
            print("player turn :", colored(self.currentPlayer, "magenta"))

    def playerChoice(self):
        choice = str(input("place a wall ( w ) or move ( m ) ?:")).lower()
        while choice not in ["w", "m"]:
            print("incorrect choice , try again")
            choice = str(
                input("place a wall ( w ) or move ( m ) ?:")).lower()

        if choice == "w":  # placement de mur
            self.placeWall()
            self.displayGrid()
        if choice == "m":  # déplacement du pion
            self.movePawn()
            self.displayGrid()

    def run(self):
        self.displayGrid()
        while not self.checkWin():      # tant qu'aucun joueur n'a gagné la partie continue
            self.displayPlayerTurn()    # Affichage du tour du joueur
            self.playerChoice()         # prise de décision par le joueur et affichage de la grille
            self.nextPlayer()           # alternance des joueurs
        self.displayWinner()


c = jeu()
c.run()
