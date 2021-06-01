import socket
import threading
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

# Ulanish
host = input(Fore.YELLOW + "[*] IP Adresingizni Kiriting: ")
port = int(input(Fore.YELLOW + "[*] Port Kiriting: "))

# Serverni boshlash
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# tinglash qismi
clients = []
nicknames = []

#hamma habarlar
def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            # Broadcasting Messages
            message = client.recv(1024)
            broadcast(message)
        except:
            # Removing And Closing Clients
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast('{} Chiqdi'.format(nickname).encode('ascii'))
            nicknames.remove(nickname)
            break


def receive():
    while True:
        # Accept Connection
        client, address = server.accept()
        print(Fore.GREEN + "Ushbu Qurilma ulandi {}".format(str(address)))

        # Request And Store Nickname
        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        # Print And Broadcast Nickname
        print(Fore.GREEN + "[*] Qurilma Nomi {}".format(nickname))
        broadcast(Fore.GREEN + "{} Qo`shildi!".format(nickname).encode('ascii'))
        client.send(Fore.GREEN + 'Serverga Ulandi!!'.encode('ascii'))

        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



receive()


