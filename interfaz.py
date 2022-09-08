import os

board = [[0 for i in range(7)] for i in range(6)]
ROW_COUNT = 6
COLUMN_COUNT = 7
TERMX, TERMY = os.get_terminal_size()

def centred(*lines):
    for line in lines:
        yield line.center(TERMX)

def print_centred(line):
    print(*centred(line))

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

def place(n,turn):
    correct = False
    row = 0
    while not correct:
        if board[row][n-1] == 0:
            board[row][n-1] = turn
            correct = True
        else:
            row += 1

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
   


def main():
    intro()
    show(board)

main()
