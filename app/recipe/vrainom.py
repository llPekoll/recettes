# [o,o,x,o]
# [o,o,o,o]
# [o,x,o,o]
# [o,o,o,x]

# from pprint import pprint


class Queen:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.is_threatened = False

    # def check_threatened(self):


class Board:
    def __init__(self, w):
        self.w = w
        self.matrix = [["0" for x in range(w)] for y in range(w)]

    def __repr__(self):
        for line in self.matrix:
            print(line)

    def mark_threat_path(self, x, y):
        # mark horizontal
        for i in range(self.w):
            self.matrix[x][i] = "x"

        # mark vertical
        for i in range(self.w):
            self.matrix[i][y] = "x"

        # mark diagonal
        for i in range(self.w):
            for j in range(self.w):
                if i + j == x + y:
                    self.matrix[i][j] = "x"
                if i - j == x - y:
                    self.matrix[i][j] = "x"

    def place_queen(self, x, y):
        self.mark_threat_path(x, y)
        self.matrix[x][y] = "1"


n = 4
board = Board(n)

board.place_queen(2, 1)

print(board)
