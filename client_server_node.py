import socket
import threading
import sys
import time
import random
from dataclasses import dataclass
from typing import List

class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Server:
    connections = []
    peers = []

    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', 10000))
        sock.listen(1)
        print("Server running...")
        while True:
            c, a = sock.accept()
            cThread = threading.Thread(target=self.connection_handler, args=(c, a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            self.peers.append(a[0])
            print(str(a[0]) + ':' + str(a[1]), " connected.")
            self.send_peers()

    def connection_handler(c, a):
        while True:
            data = c.recv(1024)
            for connection in self.connections:
                connection.send(data)
            if not data:
                print(str(a[0]) + ':' + str(a[1]), " disconnected.")
                self.connections.remove(c)
                self.peers.remove(a[0])
                c.close()
                self.send_peers()
                break

    def send_peers(self):
        p = ""
        for peer in self.peers:
            p = p + peer + ","
        for connection in self.connections:
            connection.send(b'\x11' + bytes(p, 'utf-8'))


class Client:
    def send_msg(self, sock):
        while True:
            sock.send(bytes(input(""), 'utf-8'))

    def __init__(self, address):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.connect((address, 10000))
        print("\n\nCONNECTED!!!\n")
        iThread = threading.Thread(target=self.send_msg, args=(sock,))
        iThread.daemon = True
        iThread.start()
        while True:
            data = sock.recv(1024)
            if not data:
                break
            if data[0:1] == b'\x11':
                self.update_peers(data[1:])
            else:
                print(str(data, 'utf-8'))

    def update_peers(self, peer_data):
        p2p.peers = str(peer_data, 'utf-8').split(",")[:-1]

class p2p:
    peers = ['127.0.0.1']

# <### CHANGES ###>
def try_connect(ip: str) -> bool:
    print("Trying to connect: ", colors.WARNING + ip + colors.ENDC)
    time.sleep(randint(1, 5))
    try:
        client = Client(ip)
    except KeyboardInterrupt:
        # Exit from connection
        sys.exit(0)
    except:
        # FAIL
        return False
    # OK
    return True

while True:
    try:
        server = Server()
        print("Started node at :",
        colors.WARNING +
        socket.gethostbyname(socket.gethostname()) +
        colors.ENDC)
    except KeyboardInterrupt:
        print("Exiting due KeyboardInterrupt.")
        sys.exit(0)
    except Exception as err:
        raise err
        print("Couldn't start the srever...")
        break               
    # Server started at this point, now we will
    # start reading user input
    for line in sys.stdin: 
        if 'q' == line.rstrip():
            # User asks to stop
            print('Exiting due `quit command` from user.') 
            sys.exit(0)
        if 'connect' == line.rstrip():
            # User asks to connect
            new_ip = input('Enter ip: ') # get IP to connect
            if not (try_connect(new_ip)):
                print("Failed to connect: ", colors.WARNING + ip + colors.ENDC)
                print("Waiting for new commands...")

    # except KeyboardInterrupt:
    #     sys.exit(0)