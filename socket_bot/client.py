import socket
import threading
import json
from cmd import Cmd
from socket_bot.connection import SocketConnection
from socket_bot.payload import make_payload


class Client(Cmd):
    """
    Client
    """
    prompt = ''
    intro = "[Welcome] Simple chat room client (Cli version)\n" + \
        "[Welcome] Type `help` to get help\n"

    def __init__(self, connection_args: SocketConnection):
        """
        structure
        """
        super().__init__()
        # Network connection settings
        self.__conn_params = connection_args
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__id = None
        self.__nickname = None

    def __do_payload_thread(self, flag):
        WARN = '\033[93m'
        END = '\033[0m'
        thread = threading.Thread(target=make_payload, args=())
        if flag == 'background':
            print(f'{WARN}\n(!) <background process> PAYLOAD (!){END}')
            thread.setDaemon(True)
            thread.start()
        else:
            print(f'{WARN}\n(!) PAYLOAD (!){END}')
            thread.start()
            thread.join()
        print(f'{WARN}\n(!) PAYLOAD FINISHED (!){END}')

    def __receive_message_thread(self):
        """
        Accept message thread
        """
        while True:
            # noinspection PyBroadException
            try:
                buffer = self.__socket.recv(1024).decode()
                obj = json.loads(buffer)

                print('[' + str(obj['sender_nickname']) +
                      '(' + str(obj['sender_id']) + ')' + ']', obj['message'])

                if obj['message'] == 'payload':
                    self.__do_payload_thread('main')

            except Exception as err:
                print(err)
                print('[Client] Unable to get data from server')

    def __send_message_thread(self, message):
        """
        Send message thread
        :param message: Message content
        """
        self.__socket.send(json.dumps({
            'type': 'broadcast',
            'sender_id': self.__id,
            'message': message
        }).encode())

    def start(self):
        """
        Start the client
        """
        # Get connection parameters, print info
        ip, port, _ = self.__conn_params
        print("CONNECTING ...")
        self.__conn_params.print_params()

        # Binding IP and PORT
        self.__socket.connect((ip, port))
        self.cmdloop()

    def do_login(self, args):
        """
        Login to chat room
        :param args: parameter
        """
        nickname = args.split(' ')[0]

        # Send the nickname to the server to get the user id
        self.__socket.send(json.dumps({
            'type': 'login',
            'nickname': nickname
        }).encode())
        # Try to accept data
        # noinspection PyBroadException
        try:
            buffer = self.__socket.recv(1024).decode()
            obj = json.loads(buffer)
            if obj['id']:
                self.__nickname = nickname
                self.__id = obj['id']
                print('[Client] Successfully logged in to the chat room')

                # Open the child thread for receiving data
                thread = threading.Thread(target=self.__receive_message_thread)
                thread.setDaemon(True)
                thread.start()
            else:
                print('[Client] Can\'t log in to chat room')
        except Exception:
            print('[Client] Unable to get data from server')

    def do_send(self, args):
        """
        Send a message
        :param args: parameter
        """
        message = args
        if message == 'payload':
            self.__do_payload_thread('background')
        
        # Show messages sent by yourself
        print('[' + str(self.__nickname) +
              '(' + str(self.__id) + ')' + ']', message)
        # Open the child thread for sending data
        thread = threading.Thread(
            target=self.__send_message_thread, args=(message, ))
        thread.setDaemon(True)
        thread.start()

    def do_help(self, arg):
        """
        help
        :param arg: parameter
        """
        command = arg.split(' ')[0]
        if command == '':
            print(
                '[Help] login nickname - Log in to the chat room, nickname is your chosen nickname')
            print(
                '[Help] send message - Send a message, message is the message you entered')
        elif command == 'login':
            print(
                '[Help] login nickname - Log in to the chat room, nickname is your chosen nickname')
        elif command == 'send':
            print(
                '[Help] send message - Send a message, message is the message you entered')
        else:
            print('[Help] Did not find the instruction you want to know')
