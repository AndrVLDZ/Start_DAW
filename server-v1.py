import socket
import threading
from typing import Any
import keyb

SERVER_ADDR = ('0.0.0.0', 10000)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(SERVER_ADDR)
sock.listen(1)

connections = []

def handle_event_msg(data):
    if str(data, "utf-8") == "start42\r\n":
        keyb.start()
        print("\nStarting keypress event")
    else:
        print("\nJust a msg")
        print(data)

def handler(current_conn: socket.socket, addr: Any):
    global connections
    while True:
        data: bytes = current_conn.recv(1024)
        handle_event_msg(data)
        for c in connections:
            # в этом месте тебе нужно
            # отлавливать сообщение "начать кликать"
            # и тринерить свою кнопочку
            c.send(bytes(str.encode('=>> ') + data))
        if not data:
            connections.remove(current_conn)
            current_conn.close()
            break


# Wait for an incoming connection.
while True:
    # new socket representing the connection
    conn: socket.socket
    # address of the client
    # (if IP-socket `new_addr` is a pair -> (hostaddr, port))
    addr: Any

    conn, addr = sock.accept()  # Accept new connection
    cThread = threading.Thread(target=handler, args=(conn, addr))
    cThread.daemon = True
    cThread.start()

    connections.append(conn)
    print(connections)
