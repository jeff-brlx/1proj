import socket
import pickle
from case import case
from jeu import jeu

# C:/Users/Administrateur/AppData/Local/Microsoft/WindowsApps/python3.11.exe "c:/Users/Administrateur/OneDrive - SUPINFO/Documents/GitHub/Quoridor/client.py"

host, port = ("localhost", 5566)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    socket.connect((host, port))
    print("client connecté !")
except:
    print("connexion au serveur échoué !")

    # game=jeu(5)
    # serialized_game=pickle.dumps(game)
    # socket.sendall(serialized_game)

while True:
    try:
        # Reception de la dernière version de la grille de jeu
        serialized_game = socket.recv(16384)
        game = pickle.loads(serialized_game)
        game.displayGrid()
        # reception du player_id
        serialized_data = socket.recv(16384)
        data = pickle.loads(data)
        player = int(player)
        print(player)
        # Demander de faire un choix
        choice = str(input("place a wall or move ?:"))
        if choice == "w":  # placement de mur
            game.placeWall()
            game.displayGrid()
        if choice == "m":  # déplacement du pion
            game.movePawn(player)
            game.displayGrid()

        # Envoie de la nouvelle grille
        serialized_game = pickle.dumps(game)
        socket.sendall(serialized_game)

        # reception de la grille mise à jour
        serialized_game = socket.recv(16384)
        game = pickle.loads(serialized_game)
        game.displayGrid()

    except (EOFError):
        print("Error: Connection to server lost.")
        socket.close()
        break
