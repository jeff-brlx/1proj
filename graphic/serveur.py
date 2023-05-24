import socket
import pickle
from case import case
from jeu import jeu

# C:/Users/Administrateur/AppData/Local/Microsoft/WindowsApps/python3.11.exe "c:/Users/Administrateur/OneDrive - SUPINFO/Documents/GitHub/Quoridor/serveur.py"

host,port=("",5566)
socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
socket.bind((host,port))
print("le serveur est lancé...")

# On maintient une liste de joueurs connectés
players=[]

# On maintient un compteur pour assigner un numéro unique à chaque joueur
player_number=1

# Lorsqu'un nouveau joueur se connecte au serveur
def new_player_connected(player_socket):
    global players, player_number
    # On assigne un numéro unique à ce joueur
    player_id=player_number
    player_number +=1
    # On ajoute ce joueur à la liste de joueurs connecté
    players.append((player_id,player_socket))


actual_player=1
# Démarrer un tour de jeu
def start_turn():
    global players
    game=jeu(5)

    while not game.checkWin():

        for player_id, player_socket in players:
            # Envoyer l'état actuel du jeu au joueur
            serialized_game = pickle.dumps(game)
            player_socket.sendall(serialized_game)
            #Envoie du player_id
            player=str(player_id)
            serialized_player=player.encode("utf8")
            player_socket.sendall(serialized_player)

            # Attendre une action du joueur
            serialized_game= player_socket.recv(16384)
            game = pickle.loads(serialized_game)
            game.checkWin()

            # Affichage de la nouvelle grille de jeu
            for player_id,player_socket in players:
                serialized_game = pickle.dumps(game)
                player_socket.sendall(serialized_game)
                

# Nombre maximum de joueurs dans la partie
max_players = 2

while len(players) < max_players:
    socket.listen(5)
    new_socket, address= socket.accept()
    new_player_connected(new_socket)

start_turn()

# fermer les sockets lorsque le programme s'arrête
for _, player_socket in players:
    player_socket.close()
    socket
