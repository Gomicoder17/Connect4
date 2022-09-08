import os
import sys


ROW_COUNT = 6
COLUMN_COUNT = 7
TERMX, TERMY = os.get_terminal_size()

def centred(*lines):
    for line in lines:
        yield line.center(TERMX)

def print_centred(line):
    print(*centred(line))

def check_draw(board):
    for i in board:
        for j in i:
            if j == 0:
                return False
    return True

def show(board):           
    os.system("clear || cls")
    
    # Characters for a game piece
    cells = [" ", "●", "○"]
    
    print_centred("\n" * ((TERMY - 11) // 2)) 
    print_centred("  1   2   3   4   5   6   7 ")
    for row in reversed(board):
        print_centred("+---" * 6 + "+---+")
        print_centred("| " + " | ".join([cells[u] for u in row]) + " |") 
    print_centred("+---" * 6 + "+---+")
    print_centred("")
    print_centred("")
    print_centred("")

def place(board,n,turn):
    try:
        correct = False
        row = 0
        while not correct:
            if board[row][n-1] == 0:
                board[row][n-1] = turn+1
                correct = True
            else:
                row += 1
        return correct
    except IndexError:
        return correct

def winning_move(board, piece):
    
    # Check for horizontal 4 in a row for win:
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # Check for vertical 4 in a row for win:
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # Check for upward sloping diagonal 4 in a row for win
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True
    
    # Check for downward sloping diagonal 4 in a row for win
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def intro():
    os.system("clear || cls")  
    print_centred('CONNECT 4')
    print_centred('Press enter to play')
    input()

def menu():
    os.system("clear || cls") 
    print_centred('CHOOSE HOW YOU WANT TO PLAY')
    print()
    print()
    print_centred('1:  1 player vs bot ')
    print()
    print_centred('2:     2 players    ')
    print()
    print()
    print()
    print()
    print()
    print()
    m = input('Enter the game mode: ')
    if m != '1' and m != '2':
        m = menu()
    return int(m)


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
            print_centred(f"PLAYER {turn+1}'s turn")
            print('\n\n\n\n')
            c = input('Select a column: ')
            while c != '1' and c != '2' and c != '3' and c != '4' and c != '5' and c != '6' and c != '7':
                show(board)
                print_centred(f"PLAYER {turn+1}'s turn")
                print('\n\n\n\n')
                c = input('Select a column: ')
            correct = place(board,int(c),turn)
            print(correct)
            while not correct:
                show(board)
                print_centred(f"PLAYER {turn+1}'s turn")
                print('\n\n\n\n')
                c = input('Select a column: ')
                while c != '1' and c != '2' and c != '3' and c != '4' and c != '5' and c != '6' and c != '7':
                    show(board)
                    print_centred(f"PLAYER {turn+1}'s turn")
                    print('\n\n\n\n')
                    c = input('Select a column: ')
                correct = place(board,int(c),turn)

                print(correct)


            
        else:
            ...
        draw = check_draw(board)
        victoria = winning_move(board,turn+1)
    
    

    os.system("clear || cls")
    print('\n\n\n\n') 
    if victoria:
        print_centred(f'PLAYER {turn + 1} HAS WON THE GAME')
    else: 
        print_centred("IT'S A DRAW")
    print('\n\n\n\n')
    print_centred('DO YOU WANT TO PLAY AGAIN? (y/n)')
    play = input()
    while play != 'y' and play != 'n':
        os.system("clear || cls") 
        print('\n\n\n\n')
        if victoria:
            print_centred(f'PLAYER {turn + 1} HAS WON THE GAME')
        else:
            print_centred("IT'S A DRAW")
        print('\n\n\n\n')
        print_centred('DO YOU WANT TO PLAY AGAIN? (y/n)')
        play = input()
    if play == 'y':
        main()
    else:
        sys.exit()
   

intro()
main()
