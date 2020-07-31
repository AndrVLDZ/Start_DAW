from dataclasses import dataclass, astuple


@dataclass(frozen=True)
class SocketConnection:
    ip_address: str
    port: int
    conn_type: str

    # ip, port, type = SocketConnection('127.0.0.1', 8888, 'Local')
    # print(ip)  # => '127.0.0.1'
    def __iter__(self):
        yield from astuple(self)

    def print_params(self) -> None:
        print(f'IP ADDRESS:\t\t{self.ip_address}')
        print(f'PORT:\t\t{str(self.port)}')
        print(f'TYPE:\t\t{self.conn_type}')
