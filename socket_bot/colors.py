from typing import List, Dict


class CmdColors:
    def __init__(self):
        self.__colors = {
            "HEADER":           '\033[95m',
            "OKBLUE":           '\033[94m',
            "OKGREEN":          '\033[92m',
            "WARNING":          '\033[93m',
            "FAIL":             '\033[91m',
            "ENDC":             '\033[0m',
            "BOLD":             '\033[1m',
            "UNDERLINE":        '\033[4m',
        }

    @property
    def colors(self) -> Dict[str, str]:
        return self.__colors

    def green_background(self, text: str) -> str:
        return '\x1b[6;30;42m' + text + '\x1b[0m'

    def print_all_colors(self) -> None:
        clrs = self.__colors
        printable: List[str] = ['Available colors: \n\n']
        for key in clrs.keys():
            printable.append('\t => ' + clrs[key] + key + clrs['ENDC'] + '\n')
        print(''.join(printable))

    def colorize(self, color_name: str, text: str) -> str:
        if not color_name in self.__colors.keys():
            raise ValueError('\033[93m No such color\033[0m: ' + color_name)
        return self.__colors[color_name] + text + self.__colors['ENDC']
