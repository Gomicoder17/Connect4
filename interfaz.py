import os
import sys
import time
from minimax_bin import Board
from minimax import find_best_move

ROW_COUNT = 6
COLUMN_COUNT = 7

TERMX, TERMY = os.get_terminal_size()


def centred(*lines):
    for line in lines:
        yield line.center(TERMX)


def print_centered(line):
    print(*centred(line))


def check_draw(board):
    for i in board:
        for j in i:
            if j == 0:
                return False
    return True


def show(board, clean=True):
    if clean:
        os.system("clear || cls")

    # Characters for a game piece
    cells = [" ", "●", "○"]

    print_centered("\n" * ((TERMY - 11) // 2))
    print_centered("  1   2   3   4   5   6   7 ")
    for row in board:
        print_centered("+---" * 6 + "+---+")
        print_centered("| " + " | ".join([cells[u] for u in row]) + " |")
    print_centered("+---" * 6 + "+---+")
    print_centered("")
    print_centered("")
    print_centered("")


def place(board, x, turn):
    y = len(board) - 1
    while board[y][x - 1] != 0:
        y -= 1
    board[y][x - 1] = turn + 1


def winning_move(board, piece):

    # Check for horizontal 4 in a row for win:
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check for vertical 4 in a row for win:
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check for upward sloping diagonal 4 in a row for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check for downward sloping diagonal 4 in a row for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True


def intro():
    os.system("clear || cls")
    print_centered("CONNECT 4")
    print_centered("Press enter to play")
    input()


def menu():
    os.system("clear || cls")
    print_centered("CHOOSE HOW YOU WANT TO PLAY")
    print()
    print()
    print_centered("1:  1 player vs bot ")
    print()
    print_centered("2:     2 players    ")
    print()
    print()
    print()
    print()
    print()
    print()
    m = input("Enter the game mode: ")
    if m != "1" and m != "2" and m != "3":
        m = menu()
    return int(m)


def correct(input, possible):
    if input in possible:
        return True
    return False


def main():
    board = [[0 for i in range(7)] for i in range(6)]
    m = menu()
    show(board)
    victoria = False
    turn = 1
    draw = False
    while not victoria and not draw:
        turn = 1 - turn
        show(board)
        if m == 2 or (turn == 0 and m == 1):
            print_centered(f"PLAYER {turn+1}'s turn")
            print("\n\n\n\n")
            c = input("Select a column: ")
            corr = correct(c, ["1", "2", "3", "4", "5", "6", "7"])
            while not corr:
                show(board)
                print_centered(f"PLAYER {turn+1}'s turn")
                print("\n\n\n\n")
                c = input("Select a column: ")
                corr = correct(c, ["1", "2", "3", "4", "5", "6", "7"])
            while board[0][int(c) - 1] != 0:
                show(board)
                print_centered(f"PLAYER {turn+1}'s turn")
                print("\n\n\n\n")
                c = input("Select a column: ")
                corr = correct(c, ["1", "2", "3", "4", "5", "6", "7"])
                while not corr:
                    show(board)
                    print_centered(f"PLAYER {turn+1}'s turn")
                    print("\n\n\n\n")
                    c = input("Select a column: ")
                    corr = correct(c, ["1", "2", "3", "4", "5", "6", "7"])
            place(board, int(c), turn)
        else:
            # show(board, False)
            choice = Board(board).find_best_move(9)[1]
            # choice = find_best_move(board, 7)[1]
            place(board, int(choice + 1), turn)
        show(board)
        draw = check_draw(board)
        victoria = winning_move(board, turn + 1)

    time.sleep(4)
    os.system("clear || cls")
    print("\n\n\n\n")
    if victoria:
        print_centered(f"PLAYER {turn + 1} HAS WON THE GAME")
    else:
        print_centered("IT'S A DRAW")
    print("\n\n")
    show(board, clean=False)
    print("\n\n")
    print_centered("DO YOU WANT TO PLAY AGAIN? (y/n)")
    play = input()
    while play != "y" and play != "n":
        os.system("clear || cls")
        print("\n\n\n\n")
        if victoria:
            print_centered(f"PLAYER {turn + 1} HAS WON THE GAME")
        else:
            print_centered("IT'S A DRAW")
        print("\n\n\n\n")
        print_centered("DO YOU WANT TO PLAY AGAIN? (y/n)")
        play = input()
    if play == "y":
        main()
    else:
        sys.exit()


intro()
main()
