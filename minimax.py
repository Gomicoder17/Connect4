import random as r

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2


def print_board(board):
    for row in board:
        print(" ".join([str(x) for x in row]))


def is_win(board):
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


def evaluate(board, maximizer):
    minimizer = PLAYER1 if maximizer == PLAYER2 else PLAYER2
    # print("Evaluating board for maximizer", maximizer)
    # print_board(board)
    # Traverse board horizontally
    score = 0
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            four = [
                board[row][col],
                board[row][col + 1],
                board[row][col + 2],
                board[row][col + 3],
            ]
            # Add scores for maximizer
            if not minimizer in four:
                score += four.count(maximizer) ** 2
            # Subtract scores for minimizer
            if not maximizer in four:
                score -= four.count(minimizer) ** 2
    # Traverse board vertically
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            four = [
                board[row][col],
                board[row + 1][col],
                board[row + 2][col],
                board[row + 3][col],
            ]
            # Add scores for maximizer
            if not minimizer in four:
                score += four.count(maximizer) ** 2
            # Subtract scores for minimizer
            if not maximizer in four:
                score -= four.count(minimizer) ** 2

    # Traverse board diagonally
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            four = [
                board[row][col],
                board[row + 1][col + 1],
                board[row + 2][col + 2],
                board[row + 3][col + 3],
            ]
            # Add scores for maximizer
            if not minimizer in four:
                score += four.count(maximizer) ** 2
            # Subtract scores for minimizer
            if not maximizer in four:
                score -= four.count(minimizer) ** 2

    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            four = [
                board[row][col],
                board[row + 1][col - 1],
                board[row + 2][col - 2],
                board[row + 3][col - 3],
            ]
            # Add scores for maximizer
            if not minimizer in four:
                score += four.count(maximizer) ** 2
            # Subtract scores for minimizer
            if not maximizer in four:
                score -= four.count(minimizer) ** 2
    # print("Evaluated board for maximizer", maximizer)
    # print_board(board)
    # print("Score:", score)
    # input()
    return score


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


def minimax(board, depth, player, maximizer):
    # print("Minimax called with depth", depth, "and player", player)
    if is_win(board):
        # print("Win detected", "player", player, "maximizer", maximizer)
        # print_board(board)
        return -1000 if player == maximizer else 1000
    elif is_draw(board):
        return 0
    elif depth == 0:
        return evaluate(board, maximizer)
    elif player == maximizer:
        best = -1000
        for x in range(len(board[0])):
            if board[0][x] == EMPTY:
                make_move(board, player, x)
                next_player = PLAYER2 if PLAYER1 == maximizer else PLAYER1
                best = max(best, minimax(board, depth - 1, next_player, maximizer))
                undo_move(board, x)
        return best
    else:
        best = 1000
        for x in range(len(board[0])):
            if board[0][x] == EMPTY:
                make_move(board, player, x)
                next_player = PLAYER1 if PLAYER1 == maximizer else PLAYER2
                best = min(best, minimax(board, depth - 1, next_player, maximizer))
                undo_move(board, x)
        return best


def find_best_move(board, player):
    # print("Finding best move for", player)
    # print("Board:")
    # print_board(board)
    # input()
    best_score = -1000
    best_move = None
    for x in range(len(board[0])):
        if board[0][x] == EMPTY:
            make_move(board, player, x)
            # print("Evaluating move", x)
            rival = PLAYER1 if player == PLAYER2 else PLAYER2
            score = minimax(board, 4, rival, player)
            # print(score)
            undo_move(board, x)
            if score > best_score:
                best_score = score
                best_move = x
    return best_move


board = [[EMPTY for i in range(7)] for j in range(6)]
for i, move in enumerate([4, 0, 6, 1, 3]):
    make_move(board, PLAYER1 if i % 2 == 0 else PLAYER2, move)
print_board(board)
print(find_best_move(board, PLAYER2))
