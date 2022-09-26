import os
from turtle import color
import random

RED = "\033[38;5;196m"
BLUE = "\033[38;5;45m"
YELLOW = "\033[38;5;226m"
END = "\033[m"


def print_centered(line):
    line = ' '*33 + line
    print(line)



def table(board, clean=True):
    if clean:
        os.system("clear || cls")
    char = [{'0': ' '*6, '1': RED + '  ▄▄  ' + END, '2': YELLOW + '  ▄▄  ' + END},
            {'0': ' '*6, '1': RED + '  ▀▀  ' + END, '2': YELLOW + '  ▀▀  ' + END}]
    print_centered(BLUE + '╔' + ('═'*6 + '╦')*6 + '═'*6 + '╗' + END)
    for n, row in enumerate(board):
        for i in range(2):
            linea = BLUE + '║'
            for elem in row:
                linea += char[i][elem] + BLUE + '║'
            linea += END
            print_centered(linea)
        if n != len(board) - 1:
            print_centered(BLUE + '╠' + ('═'*6 + '╬')*6 + '═'*6 + '╣' + END)
        else:
            print_centered(BLUE + '╚' + ('═'*6 + '╩')*6 + '═'*6 + '╝' + END)


if __name__ == '__main__':
    board = [[str(random.randint(0, 2)) for i in range(7)] for j in range(6)]
    table(board, True)
