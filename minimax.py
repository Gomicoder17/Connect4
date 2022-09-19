import random as r

EMPTY = 0
PLAYER1 = 1
PLAYER2 = 2


def print_board(board):
    for row in board:
        print(" ".join([str(x) for x in row]))
    print()


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
    # Traverse board diagonally 2
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


def evaluate(board):
    score = 0
    for row in range(len(board)):
        for col in range(len(board[0]) - 3):
            four = [
                board[row][col],
                board[row][col + 1],
                board[row][col + 2],
                board[row][col + 3],
            ]
            if not PLAYER2 in four:
                score += (four.count(PLAYER1)) ** 2
            if not PLAYER1 in four:
                score -= (four.count(PLAYER2)) ** 2
    for row in range(len(board) - 3):
        for col in range(len(board[0])):
            four = [
                board[row][col],
                board[row + 1][col],
                board[row + 2][col],
                board[row + 3][col],
            ]
            if not PLAYER2 in four:
                score += (four.count(PLAYER1)) ** 2
            if not PLAYER1 in four:
                score -= (four.count(PLAYER2)) ** 2
    for row in range(len(board) - 3):
        for col in range(len(board[0]) - 3):
            four = [
                board[row][col],
                board[row + 1][col + 1],
                board[row + 2][col + 2],
                board[row + 3][col + 3],
            ]
            if not PLAYER2 in four:
                score += (four.count(PLAYER1)) ** 2
            if not PLAYER1 in four:
                score -= (four.count(PLAYER2)) ** 2
    for row in range(len(board) - 3):
        for col in range(3, len(board[0])):
            four = [
                board[row][col],
                board[row + 1][col - 1],
                board[row + 2][col - 2],
                board[row + 3][col - 3],
            ]
            if not PLAYER2 in four:
                score += (four.count(PLAYER1)) ** 2
            if not PLAYER1 in four:
                score -= (four.count(PLAYER2)) ** 2
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


def minimax(board, depth, player, alpha=float("-inf"), beta=float("inf")):
    if is_win(board):
        return 1000 if player == PLAYER2 else -1000, None
    elif is_draw(board):
        return 0, None
    elif depth == 0:
        return evaluate(board), None
    elif player == PLAYER1:
        best, bestMove = -1000, None
        for x in range(len(board[0])):
            if board[0][x] == EMPTY:
                make_move(board, player, x)
                score, _ = minimax(board, depth - 1, PLAYER2, alpha, beta)
                if score >= best:
                    best, bestMove = score, x
                alpha = max(alpha, best)
                undo_move(board, x)
                if alpha >= beta:
                    return float("inf"), bestMove
        return best, bestMove
    elif player == PLAYER2:
        best, bestMove = 1000, None
        for x in range(len(board[0])):
            if board[0][x] == EMPTY:
                make_move(board, player, x)
                score, _ = minimax(board, depth - 1, PLAYER1, alpha, beta)
                if score <= best:
                    best, bestMove = score, x
                beta = min(beta, best)
                undo_move(board, x)
                if alpha >= beta:
                    return float("-inf"), bestMove
        return best, bestMove


def find_best_move(board, depth=3):
    player = (sum([sum(row) for row in board]) % 2) + 1
    return minimax(board, depth, player)


if __name__ == "__main__":
    board = [[EMPTY for i in range(7)] for j in range(6)]
    for i, move in enumerate([0, 1, 2, 3, 4, 5, 6]):
        make_move(board, PLAYER1, move)
        # print_board(board)
        print(evaluate(board))
        undo_move(board, move)
    print_board(board)
    print(minimax(board, 7, PLAYER1))
