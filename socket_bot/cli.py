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
        name, conn = opt
        if conn != ():
            ip, port, info = conn
        else:
            ip, port, info = ('<IP>', '<PORT>', 'Specify all params')
        NAME = cl.colorize('WARNING', name)
        IP = cl.colorize('OKGREEN', ip)
        PORT = cl.colorize('OKBLUE', str(port))
        print('\t\t', num, ') ', NAME, ':', info,
              '\n\t\t\t=> ', IP, ' : ', PORT)


def start_server(conn_opts: Dict[int, Tuple[Any]] = ''):
    """
    Start server, ask user for IP,PORT parameters
    """
    CONN_OPTS: Dict[int, Tuple[Any]] = {
        1: ('Stdandard: ',      SocketConnection('127.0.0.1', 8888, 'Start server/client locally')),
        2: ('VLDZ ANDROID: ',   SocketConnection('0.0.0.0', 10000, 'Run server on Android')),
        3: ('Manual: Connection in LAN', ()),
    }

    cl = CmdColors()
    print_options(CONN_OPTS)

    try:
        choice = int(input('Type option: '))

        if choice not in CONN_OPTS.keys():
            raise ValueError

        conn: SocketConnection = CONN_OPTS[choice][1]
        if conn == ():
            _ip = input('Type IP: ')
            _port = int(input('Type PORT: '))
            s = Server(SocketConnection(_ip, _port, CONN_OPTS[choice][0]))
        else:
            s = Server(conn)
        s.start()
        s.cmdloop()

        print(cl.colorize('OKGREEN', '\nGot it, working on it...\n'))

    except ValueError:
        print(cl.colorize('FAIL', '\n=> Wrong value! Try again.'))
        start_server()

    except KeyboardInterrupt:
        print(cl.colorize('FAIL', '\nExiting...'))
        return


def connect_client(conn_opts: Dict[int, Tuple[Any]] = ''):
    """
    Start client, ask user for IP,PORT parameters
    """
    CONN_OPTS: Dict[int, Tuple[Any]] = {
        1: ('Stdandard: ',      SocketConnection('127.0.0.1', 8888, 'Connect client locally')),
        2: ('VLDZ ANDROID: ',   SocketConnection('192.168.0.100', 10000, 'Connect to server running on Android')),
        3: ('Manual: Connection in LAN', ()),
    }

    if conn_opts != '':
        CONN_OPTS = conn_opts

    cl = CmdColors()
    print_options(CONN_OPTS)

    try:
        choice = int(input('Type option: '))

        if choice not in CONN_OPTS.keys():
            raise ValueError

        conn: SocketConnection = CONN_OPTS[choice][1]
        if conn == ():
            _ip = input('Type IP: ')
            _port = int(input('Type PORT: '))
            c = Client(SocketConnection(_ip, _port, CONN_OPTS[choice][0]))
        else:
            c = Client(conn)
        c.start()

        print(cl.colorize('OKGREEN', '\nGot it, working on it...\n'))

    except ValueError:
        print(cl.colorize('FAIL', '\n=> Wrong value! Try again.'))
        connect_client()

    except KeyboardInterrupt:
        print(cl.colorize('FAIL', '\nExiting...'))
        return
