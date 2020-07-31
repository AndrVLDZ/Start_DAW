import socket
import threading
import json
from cmd import Cmd
from typing import List
from socket_bot.connection import SocketConnection
from socket_bot.colors import CmdColors


class Server(Cmd):
    """
    Server class
    """
    prompt = '\033[93m(SocketServer console)\033[0m'

    def __init__(self, connection_args: SocketConnection):
        """
        structure
        """
        # Network connection settings
        self.__conn_params = connection_args
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__connections: List[socket.socket] = list()
        self.__nicknames: List[str] = list()

    @property
    def connections(self) -> List[socket.socket]:
        return self.__connections

    def __broadcast_server_msg(self, msg: str = 'I AM SERVER'):
        for ind in range(1, len(self.__connections)):
            self.__connections[ind].send(
                json.dumps({
                    'sender_id': 0,
                    'sender_nickname': '<SERVER>',
                    'message': msg}).encode()
            )

    def do_payload(self, args):
        self.__broadcast_server_msg('payload')

    def __await_commands(self):
        cl = CmdColors()
        print('\n', cl.green_background('SERVER WAITING FOR YOUR COMMANDS'), '\n')
        self.cmdloop()

    def __user_thread(self, user_id):
        """
        User child thread
        :param user_id: User id
        """
        connection = self.__connections[user_id]
        nickname = self.__nicknames[user_id]
        print('[Server] user', user_id, nickname, 'Join the chat room')
        self.__broadcast(message='user ' + str(nickname) +
                         '(' + str(user_id) + ')' + 'Join the chat room')

        # Listen
        while True:
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # Parse into json data
                obj = json.loads(buffer)
                # If it is a broadcast instruction
                if obj['type'] == 'broadcast':
                    self.__broadcast(obj['sender_id'], obj['message'])
                else:
                    print('[Server] Unable to parse json packet:',
                          connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] Connection failure:',
                      connection.getsockname(), connection.fileno())
                self.__connections[user_id].close()
                self.__connections[user_id] = None
                self.__nicknames[user_id] = None

    def __broadcast(self, user_id=0, message=''):
        """
        broadcast
        :param user_id: User id (0 is system)
        :param message: Broadcast content
        """
        for i in range(1, len(self.__connections)):
            if user_id != i:
                self.__connections[i].send(json.dumps({
                    'sender_id': user_id,
                    'sender_nickname': self.__nicknames[user_id],
                    'message': message
                }).encode())

    def start(self):
        """
        Start the server
        """
        # Get connection parameters, print info
        ip, port, _ = self.__conn_params
        print("STARTING ...")
        self.__conn_params.print_params()

        # Binding IP and PORT
        self.__socket.bind((ip, port))

        # Enable monitoring
        self.__socket.listen(10)
        print('[Server] Server is running......')

        # Clear connection
        self.__connections.clear()
        self.__nicknames.clear()
        self.__connections.append(None)
        self.__nicknames.append('System')

        # Start listening
        while True:
            connection, _address = self.__socket.accept()
            print('[Server] Received a new connection',
                  connection.getsockname(), connection.fileno())

            # Try to accept data
            # noinspection PyBroadException
            try:
                buffer = connection.recv(1024).decode()
                # Parse into json data
                obj = json.loads(buffer)
                # If it is a connection command,
                # then a new user number is returned to receive the user connection
                if obj['type'] == 'login':
                    self.__connections.append(connection)
                    self.__nicknames.append(obj['nickname'])
                    connection.send(json.dumps({
                        'id': len(self.__connections) - 1
                    }).encode())

                    # Open a new thread
                    thread = threading.Thread(
                        target=self.__user_thread, args=(len(self.__connections) - 1, ))
                    thread.setDaemon(True)
                    thread.start()
                
                    self.__await_commands()
                else:
                    print('[Server] Unable to parse json packet:',
                          connection.getsockname(), connection.fileno())
            except Exception:
                print('[Server] Unable to accept data:',
                      connection.getsockname(), connection.fileno())
