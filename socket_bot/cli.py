from typing import *
from dataclasses import dataclass, astuple

from socket_bot.server import Server
from socket_bot.client import Client
from socket_bot.colors import CmdColors
from socket_bot.connection import SocketConnection


def print_logo(logo=''):
    LOGO_DAFAULT = """\033[93m

   /\                 /\\
  / \\'._   (\_/)   _.'/ \\
 /_.''._'--('.')--'_.''._\\
 | \_ / `;=/ " \=;` \ _/ |
  \/ `\__|`\___/`|__/`  \/
bot`      \(/|\)/       `
           " ` "
\033[0m
"""
    if logo != '':
        print(logo)
    else:
        print(LOGO_DAFAULT)


def print_options(conn_opts):
    cl = CmdColors()
    print(cl.colorize('HEADER', 'Enter connection type:'))
    for num, opt in conn_opts.items():
        name, info, ip, port = opt
        NAME = cl.colorize('WARNING', name)
        IP = cl.colorize('OKGREEN', ip)
        PORT = cl.colorize('OKBLUE', port)
        print('\t\t', num, ') ', NAME, ':', info,
              '\n\t\t\t=> ', IP, ' : ', PORT)


def start_server():
    """
    Start server, ask user for IP,PORT parameters
    """
    CONN_OPTS: Dict[int, Tuple[Any]] = {
        1: ('Stdandard: ',  'Start server/client locally', '127.0.0.1', '8888'),
        2: ('LAN: ',        'Connection in your local network', '0.0.0.0', '<specify PORT>'),
        3: ('LAN[+]: ',     'Connection in your local network', '<specify IP>', '<specify PORT>'),
    }

    cl = CmdColors()
    print_options(CONN_OPTS)

    try:
        s: Server
        choice = int(input('Type option: '))

        if choice not in CONN_OPTS.keys():
            raise ValueError

        opt_name: str = CONN_OPTS[choice][0] + CONN_OPTS[choice][1]

        if choice == 1:
            s = Server(SocketConnection('127.0.0.1', 8888, opt_name))
        elif choice == 2:
            _port = int(input('Type PORT: '))
            s = Server(SocketConnection('0.0.0.0', _port, opt_name))
        elif choice == 3:
            _ip = input('Type IP: ')
            _port = int(input('Type PORT: '))
            s = Server(SocketConnection(_ip, _port, opt_name))

        s.start()
        print(cl.colorize('OKGREEN', '\nGot it, working on it...\n'))

    except ValueError:
        print(cl.colorize('FAIL', '\n=> Wrong value! Try again.'))
        start_server()

    except KeyboardInterrupt:
        print(cl.colorize('FAIL', '\nExiting...'))
        return


def connect_client():
    """
    Start client, ask user for IP,PORT parameters
    """
    CONN_OPTS: Dict[int, Tuple[Any]] = {
        1: ('Stdandard: ',  'Start server/client locally', '127.0.0.1', '8888'),
        2: ('LAN[+]: ',     'Connection in your local network', '<specify IP>', '<specify PORT>'),
    }

    cl = CmdColors()
    print_options(CONN_OPTS)

    try:
        c: Client
        choice = int(input('Type option: '))

        if choice not in CONN_OPTS.keys():
            raise ValueError

        opt_name: str = CONN_OPTS[choice][0] + CONN_OPTS[choice][1]

        if choice == 1:
            c = Client(SocketConnection('127.0.0.1', 8888, opt_name))
        elif choice == 2:
            _ip = input('Type IP: ')
            _port = int(input('Type PORT: '))
            c = Client(SocketConnection(_ip, _port, opt_name))

        c.start()
        print(cl.colorize('OKGREEN', '\nGot it, working on it...\n'))

    except ValueError:
        print(cl.colorize('FAIL', '\n=> Wrong value! Try again.'))
        connect_client()

    except KeyboardInterrupt:
        print(cl.colorize('FAIL', '\nExiting...'))
        return
