import socket
import threading
import random


def handle_client(conn, player_id):
    global current_player

    while True:
        data = conn.recv(1024)
        if not data:
            break
        if player_id == current_player:
            for p in players:
                if p != conn:
                    p.sendall(data)
            current_player = (current_player + 1) % len(players)
    conn.close()


host, port = "192.168.182.74", 12345
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(4)

players = []
num_players = 4
current_player = random.randint(0, num_players - 1)

for i in range(num_players):
    conn, addr = server.accept()
    print("Joueur", i, "connecté depuis", addr)
    players.append(conn)
    thread = threading.Thread(target=handle_client, args=(conn, i))
    thread.start()
