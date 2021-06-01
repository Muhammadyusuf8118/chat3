import socket
import threading
import colorama
from colorama import Fore, Back, Style
colorama.init(autoreset=True)

server_ip = input(Fore.YELLOW + "[*] Serverning Ip ni Kriting:")
server_port = int(input(Fore.YELLOW + "[*] Port:"))


# sizning nick ismingiz
nickname = input(Fore.YELLOW + "[*]Ismingizni Korotong[*]: ")

# serverga ulanish
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

# tinglanmoqda va serverga uzatilmoqda
def receive():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(Fore.GREEN + message)
        except:
            # Close Connection When Error
            print(Fore.RED + "An error occured!")
            client.close()
            break



# Sending Messages To Server
def write():
    while True:
        message = '{}: {}'.format(Fore.GREEN + nickname, input('[*]'))
        client.send(message.encode('ascii'))

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
