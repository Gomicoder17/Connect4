class Board:
    def __init__(self, board=None):
        self.WIDTH = 7
        self.HEIGHT = 6
        self.EMPTY = "0"
        self.PLAYER1 = "1"
        self.PLAYER2 = "2"

        self.player = self.PLAYER1
        self.state1 = 0
        self.state2 = 0
        self.heights = [0, 7, 14, 21, 28, 35, 42]

        if board:
            self.convert2bin(board)

    def is_win(self):
        state = self.state1 if self.player == self.PLAYER2 else self.state2
        for step in (1, 6, 7, 8):
            if state & (state >> step) & (state >> 2 * step) & (state >> 3 * step) != 0:
                return True
        return False

    def is_draw(self):
        return self.state1 & self.state2 == int(
            "0111111011111101111110111111011111101111110111111", 2
        )

    def available_fours(self, state):
        count = 0
        aid = int("0111111011111101111110111111011111101111110111111", 2)
        state = state ^ aid
        for step in (1, 6, 7, 8):
            count += bin(
                state & (state >> step) & (state >> 2 * step) & (state >> 3 * step)
            ).count("1")
        return count

    def count_threes(self, state, state_rival):
        state_rival = state_rival | int(
            "1111111000000100000010000001000000100000010000001000000", 2
        )
        count = 0
        for step in (1, 6, 7, 8):
            n_threes = state & (state >> step) & (state >> 2 * step)
            n_threes = (
                ((n_threes >> step) ^ state_rival)
                | ((n_threes << 3 * step) ^ state_rival)
            ) ^ state_rival
            count += bin(n_threes).count("1")
        return count

    def count_twos(self, state, state_rival):
        state_rival = state_rival | int(
            "1111111000000100000010000001000000100000010000001000000", 2
        )
        count = 0
        for step in (1, 6, 7, 8):
            n_twos = state & (state >> step)
            n_twos = (
                ((n_twos >> step) ^ state_rival) | ((n_twos << 2 * step) ^ state_rival)
            ) ^ state_rival
            count += bin(n_twos).count("1")
        return count

    def count_ones(self, state, state_rival):
        # SHIFT RIGHT (Down) with 1s
        barrier = int(
            "11111111000000100000010000001000000100000010000001000000",
            2,
        )
        toggle = int("1111111111111111111111111111111111111111111111111", 2)
        mask = state | barrier | state_rival
        count = 0
        # Match 1000
        for step in (1, 8, 7, 6):
            n_ones = (
                state
                & ((mask >> step) ^ toggle)
                & ((mask >> 2 * step) ^ toggle)
                & ((mask >> 3 * step) ^ toggle)
            )
            count += bin(n_ones).count("1")
            # print("1000", bin(n_ones).count("1"))
        # Match 0100
        for step in (8, 7, 6):
            n_ones = (
                state
                & ((mask << step | 2**step - 1) ^ toggle)
                & ((mask >> step) ^ toggle)
                & ((mask >> 2 * step) ^ toggle)
            )
            count += bin(n_ones).count("1")
            # print("0100", bin(n_ones).count("1"))
        # Match 0010
        for step in (8, 7, 6):
            n_ones = (
                state
                & ((mask >> step) ^ toggle)
                & ((mask << step | 2**step - 1) ^ toggle)
                & ((mask << 2 * step | 2 ** (2 * step) - 1) ^ toggle)
            )
            count += bin(n_ones).count("1")
            # print("0010", bin(n_ones).count("1"))
        # Match 0001
        for step in (8, 7, 6):
            n_ones = (
                state
                & ((mask << step | 2**step - 1) ^ toggle)
                & ((mask << 2 * step | 2 ** (2 * step) - 1) ^ toggle)
                & ((mask << 3 * step | 2 ** (3 * step) - 1) ^ toggle)
            )
            count += bin(n_ones).count("1")
            # print("0001", bin(n_ones).count("1"))
        return count

    def make_move(self, col):
        if self.player == self.PLAYER1:
            l = 1 << self.heights[col]
            self.state1 = self.state1 ^ l
        else:
            l = 1 << self.heights[col]
            self.state2 = self.state2 ^ l
        self.heights[col] += 1
        self.player = self.PLAYER2 if self.player == self.PLAYER1 else self.PLAYER1

    def undo_move(self, col):
        self.heights[col] -= 1
        player = (
            self.PLAYER1 if self.state1 & (1 << self.heights[col]) else self.PLAYER2
        )
        if player == self.PLAYER1:
            l = 1 << self.heights[col]
            self.state1 = self.state1 ^ l
        else:
            l = 1 << self.heights[col]
            self.state2 = self.state2 ^ l
        self.player = self.PLAYER2 if self.player == self.PLAYER1 else self.PLAYER1

    def place(self, player, col):
        if player == self.PLAYER1:
            l = 1 << self.heights[col]
            self.state1 = self.state1 ^ l
        else:
            l = 1 << self.heights[col]
            self.state2 = self.state2 ^ l
        self.heights[col] += 1

    def evaluate(self):
        score = 0
        score += self.count_ones(self.state1, self.state2)
        score -= self.count_ones(self.state2, self.state1)
        score += self.count_twos(self.state1, self.state2)
        score -= self.count_twos(self.state2, self.state1)
        score += self.count_threes(self.state1, self.state2) ** 2
        score -= self.count_threes(self.state2, self.state1) ** 2
        return score

    def convert2bin(self, board):
        self.state1 = 0
        self.state2 = 0
        ones, twos = 0, 0
        for row in reversed(board):
            for x, el in enumerate(row):
                if str(el) == self.PLAYER1:
                    self.place(self.PLAYER1, x)
                    ones += 1
                elif str(el) == self.PLAYER2:
                    self.place(self.PLAYER2, x)
                    twos += 1
        self.player = str((ones + twos) % 2 + 1)

    def convert2board(self):
        state1 = bin(self.state1)[2:].zfill(64)[::-1]
        state2 = bin(self.state2)[2:].zfill(64)[::-1]
        board = []
        for y in range(6):
            board.append([])
            for x in range(7):
                i = 7 * x + (5 - y)
                c = (
                    self.PLAYER1
                    if state1[i] == "1"
                    else self.PLAYER2
                    if state2[i] == "1"
                    else self.EMPTY
                )
                board[y].append(c)
        return board

    def find_best_move(self, depth=3):
        print("Finding best move for player", self.player)
        return minimax(self, depth, self.player)

    def print(self):
        board = self.convert2board()
        for row in board:
            print(" ".join([str(e) for e in row]))
        print(bin(self.state1)[2:].zfill(64))
        print(bin(self.state2)[2:].zfill(64))
        print("Player", self.player)


def minimax(board, depth, player, alpha=float("-inf"), beta=float("inf")):
    if board.is_win():
        return 1000 if player == board.PLAYER2 else -1000, None
    elif board.is_draw():
        return 0, None
    elif depth == 0:
        return board.evaluate(), None
    elif player == board.PLAYER1:
        best, bestMove = -1000, None
        for x in range(7):
            if board.heights[x] % 7 < 6:
                board.make_move(x)
                score, _ = minimax(board, depth - 1, board.PLAYER2, alpha, beta)
                if score >= best:
                    best, bestMove = score, x
                alpha = max(alpha, best)
                board.undo_move(x)
                if alpha >= beta or best == 1000:
                    return float("inf"), None
        return best, bestMove
    elif player == board.PLAYER2:
        best, bestMove = 1000, None
        for x in range(7):
            if board.heights[x] % 7 < 6:
                board.make_move(x)
                score, _ = minimax(board, depth - 1, board.PLAYER1, alpha, beta)
                if score <= best:
                    best, bestMove = score, x
                beta = min(beta, best)
                board.undo_move(x)
                if alpha >= beta or best == -1000:
                    return float("-inf"), None

        return best, bestMove


if __name__ == "__main__":
    board = [
        "0000000",
        "0000000",
        "0000000",
        "0000000",
        "0000000",
        "0000000",
    ]
    bin_board = Board(board)
    DEPTH = 9
    print(bin_board.find_best_move(depth=DEPTH))
