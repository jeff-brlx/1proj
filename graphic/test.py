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
            serialized_game = my_socket.recv(16384)
            self.grid = pickle.loads(serialized_game)

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

        # fonction permettant aux clients de jouer ou re9voir le plateau
        def play():
            self.drawCellHeight()

            if self.currentPlayer == self.player_id:
                while self.currentPlayer == self.player_id:
                    self.handlingGameEvents()
                    self.displayScreen()
                    self.drawPlayerDirection()
                    self.displayHover()
                    if self.ShowSettingsMenu == True:
                        self.displaySettingsMenu()
                    pygame.display.flip()
                    self.clock.tick(30)

                    serialized_game = pickle.dumps(self.grid)
                    my_socket.sendall(serialized_game)

                    data = [str(self.player1barriers), str(self.player2barriers), str(
                        self.player3barriers), str(self.player4Barriers), str(self.currentPlayer)]
                    print("data sent to server after a play ( player) ", data)
                    serialized_data = pickle.dumps(data)
                    my_socket.sendall(serialized_data)

            elif self.currentPlayer != self.player_id:
                while self.currentPlayer != self.player_id:

                    self.displayScreen()
                    if self.ShowSettingsMenu == True:
                        self.displaySettingsMenu()

                    pygame.display.flip()
                    self.clock.tick(30)

                    # Receive the signal from the server
                    signal = my_socket.recv(1024)

                    # Only try to read the game data if it's their turn
                    if signal == b'YOUR_TURN':
                        serialized_game = my_socket.recv(16384)
                        self.grid = pickle.loads(serialized_game)

                        serialized_data = my_socket.recv(16384)
                        data = pickle.loads(serialized_data)

                        # After each turn, rotate to the next player
                        print("data received after a play ( client)", data)
                        print("data 0", data[0])
                        print("self.grid", self.grid)
                        self.player1barriers = int(data[0])
                        self.player2barriers = int(data[1])
                        self.player3barriers = int(data[2])
                        self.player4Barriers = int(data[3])
                        self.currentPlayer = int(data[4])
                        print(data[0])

        try:
            initVar()
            play()

        except (EOFError):
            print("Error: Connection to server lost.")
            my_socket.close()



    def serveur(self):
        host, port = ("", 5566)
        my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        my_socket.bind((host, port))
        print("le serveur est lancé...")

        self.player_number = 0
        self.players = []

        def new_player_connected(player_socket):
            self.player_number += 1
            self.player_id = self.player_number
            self.players.append((self.player_id, player_socket))

        # initialisatation des choix faits par le serveur
        def initVar():
            for self.player_id, player_socket in self.players:
                serialized_game = pickle.dumps(self.grid)
                player_socket.sendall(serialized_game)

                data = [str(self.player1barriers), str(self.player2barriers), str(self.player3barriers), str(self.player4Barriers), str(self.currentPlayer), str(
                    self.player_id), str(self.gridSize), str(self.nbBarrierPerPlayer), str(self.totalBot), str(self.totalHuman), str(self.nbPlayers), str(self.fakeGridSize)]
                print("data send for init (serveur)", data)
                serialized_data = pickle.dumps(data)
                player_socket.sendall(serialized_data)

        def runGame():
            while not self.checkWin():
                # Only receive data from the player if it's their turn.

                for self.player_id, player_socket in self.players:
                    if self.player_id == self.currentPlayer:
                        lastPlayer = self.player_id

                        serialized_game = player_socket.recv(16384)
                        self.grid = pickle.loads(serialized_game)

                        serialized_data = player_socket.recv(16384)
                        data = pickle.loads(serialized_data)
                        # After each turn, rotate to the next player
                        print("data receive after a play (player)", data)
                        self.player1barriers = int(data[0])
                        self.player2barriers = int(data[1])
                        self.player3barriers = int(data[2])
                        self.player4Barriers = int(data[3])
                        self.currentPlayer = int(data[4])

                data = [str(self.player1barriers), str(self.player2barriers), str(
                        self.player3barriers), str(self.player4Barriers), str(self.currentPlayer)]

                for self.player_id, player_socket in self.players:

                    player_socket.sendall(b'YOUR_TURN')
                    serialized_game = pickle.dumps(self.grid)
                    player_socket.sendall(serialized_game)
                    # data 0 correspond au plateau wtfff

                    serialized_data = pickle.dumps(data)
                    print("data sent to client after a play  (serveur)", data)
                    player_socket.sendall(serialized_data)

        while len(self.players) < self.nbPlayers:
            my_socket.listen(self.nbPlayers)
            new_socket, address = my_socket.accept()
            new_player_connected(new_socket)

        initVar()
        runGame()

        for _, player_socket in self.players:
            player_socket.close()

 
















 class Client:
        def __init__(self, jeu):
        self.server_address = ("localhost", 9999)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.jeu = jeu

    def connect(self):
        self.client_socket.connect(self.server_address)

    def send_data(self, data):
        serialized_data = pickle.dumps(data)
        self.client_socket.send(serialized_data)

    def receive_data(self):
        data = self.client_socket.recv(2048)
        return data

    def receive_host_choices(self):
        serialized_data = self.client_socket.recv(16384)
        data = pickle.loads(serialized_data)

        print("current player", int(data[4]))
        print("grid size", int(data[6]))
        print("nb barrier", int(data[7]))
        print("bot ", int(data[8]))
        print("human", int(data[9]))
        print("nb player", int(data[10]))

        return data

    def close(self):
        self.client_socket.close()