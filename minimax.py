import random as r

EMPTY = 0
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


def evaluate(board, player):
    score = 0
    max_score = 0
    rival = PLAYER1 if player == PLAYER2 else PLAYER2
    # Traverse board horizontally
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            four = [
                board[row][col],
                board[row][col + 1],
                board[row][col + 2],
                board[row][col + 3],
            ]
            if not rival in four:
                score += 1
            max_score += 1
    # Traverse board vertically
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            four = [
                board[row][col],
                board[row + 1][col],
                board[row + 2][col],
                board[row + 3][col],
            ]
            if not rival in four:
                score += 1
            max_score += 1

    # Traverse board diagonally
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            four = [
                board[row][col],
                board[row + 1][col + 1],
                board[row + 2][col + 2],
                board[row + 3][col + 3],
            ]
            if not rival in four:
                score += 1
            max_score += 1

    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            four = [
                board[row][col],
                board[row + 1][col - 1],
                board[row + 2][col - 2],
                board[row + 3][col - 3],
            ]
            if not rival in four:
                score += 1
            max_score += 1
    return (2 * score / max_score - 1) * 10


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
    # print("minimax", board, depth, player)
    winner = check_winner(board)
    if winner:
        return 1000 if winner == player else -1000
    elif is_draw(board):
        return 0
    elif depth == 0:
        return evaluate(board, player)
    elif player == PLAYER1:
        best = -1000
        for x in range(len(board[0])):
            if board[0][x] == 0:
                make_move(board, player, x)
                best = max(best, minimax(board, depth - 1, PLAYER2))
                undo_move(board, x)
        return best
    elif player == PLAYER2:
        best = 1000
        for x in range(len(board[0])):
            if board[0][x] == 0:
                make_move(board, player, x)
                best = min(best, minimax(board, depth - 1, PLAYER1))
                undo_move(board, x)
        return best


def find_best_move(board, player):
    best_score = 1000
    best_move = None
    for x in range(len(board[0])):
        if board[0][x] == 0:
            make_move(board, player, x)
            score = minimax(board, 0, PLAYER1 if player == PLAYER2 else PLAYER2)
            undo_move(board, x)
            if score < best_score:
                best_score = score
                best_move = x
    return best_move


board = [[EMPTY for i in range(7)] for j in range(6)]
print(find_best_move(board, PLAYER1))
