import random as r

EMPTY = " "
PLAYER1 = 1
PLAYER2 = 2


def check_winner(board):
    # Traverse board horizontally
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            if (
                board[row][col]
                == board[row][col + 1]
                == board[row][col + 2]
                == board[row][col + 3]
                != EMPTY
            ):
                return board[row][col]
    # Traverse board vertically
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            if (
                board[row][col]
                == board[row + 1][col]
                == board[row + 2][col]
                == board[row + 3][col]
                != EMPTY
            ):
                return board[row][col]
    # Traverse board diagonally
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            if (
                board[row][col]
                == board[row + 1][col + 1]
                == board[row + 2][col + 2]
                == board[row + 3][col + 3]
                != EMPTY
            ):
                return board[row][col]
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            if (
                board[row][col]
                == board[row + 1][col - 1]
                == board[row + 2][col - 2]
                == board[row + 3][col - 3]
                != EMPTY
            ):
                return board[row][col]
    return None


def is_draw(board):
    for row in board:
        for col in row:
            if col == EMPTY:
                return False
    return True


def make_move(board, player, x):
    y = len(board) - 1
    while board[y][x] != EMPTY:
        y -= 1
    board[y][x] = player


def undo_move(board, x):
    y = 0
    while board[y][x] == EMPTY:
        y += 1
    board[y][x] = EMPTY


def minimax(board, depth, player):
    winner = check_winner(board)
    if winner:
        return 1 if winner == player else -1
    elif is_draw(board):
        return 0
    elif depth == 0:
        return r.random() - 0.5  # CHANGE FOR A GOOD EVALUATION FUNCTION
    elif player == PLAYER1:
        best = -1
        for x in range(len(board[0])):
            if board[0][x] == " ":
                make_move(board, player, x)
                best = max(best, minimax(board, depth - 1, PLAYER2))
                undo_move(board, x)
        return best
    elif player == PLAYER2:
        best = 1
        for x in range(len(board[0])):
            if board[0][x] == " ":
                make_move(board, player, x)
                best = min(best, minimax(board, depth - 1, PLAYER1))
                undo_move(board, x)
        return best


def find_best_move(board, player):
    best_score = -1
    best_move = None
    for x in range(len(board[0])):
        if board[0][x] == " ":
            make_move(board, player, x)
            score = minimax(board, 6, PLAYER1 if player == PLAYER2 else PLAYER2)
            print(score)
            undo_move(board, x)
            if score > best_score:
                best_score = score
                best_move = x
    return best_move


board = [[EMPTY for i in range(7)] for j in range(6)]

print(find_best_move(board, PLAYER1))
