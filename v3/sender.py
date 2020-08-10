import telnetlib

def print_logo(logo=''):
    LOGO_DAFAULT = """\033[93m

   /\                 /\\
  / \\'._   (\_/)   _.'/ \\
 /_.''._'--('.')--'_.''._\\
 | \_ / `;=/ " \=;` \ _/ |
  \/ `\__|`\___/`|__/`  \/
   `      \(/|\)/        `
           " ` "
     DAW_Start_By_VLDZ
\033[0m
"""
    if logo != '':
        print(logo)
    else:
        print(LOGO_DAFAULT)

print_logo()

port = int(input('\nTELL ME THE FUCKING PORT:'))
ip_1 = str(input('Node_1 IP: '))
ip_2 = str(input('Node_2 IP: '))
node_1 = telnetlib.Telnet(ip_1, port)
node_2 = telnetlib.Telnet(ip_2, port)

while True:
    symbol = str(input('==> '))
    if symbol == 's':
        node_1.write(b's\r\n')
        node_2.write(b's\r\n')
    elif symbol == 'n':
        node_1.write(b'n\r\n')
        node_2.write(b'n\r\n')
    elif symbol == 'b':
        node_1.write(b'b\r\n')
        node_2.write(b'b\r\n')
    else:
        node_1.write(bytes(str.encode(symbol)))
        node_2.write(bytes(str.encode(symbol)))