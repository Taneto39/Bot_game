from sudoku_f import *

s = [[0, 0, 7, 4, 0, 1, 0, 2, 0],
     [8, 0, 0, 0, 0, 0, 0, 0, 7],
     [0, 0, 0, 0, 0, 3, 0, 0, 0],
     [0, 5, 0, 0, 0, 0, 6, 0, 0],
     [0, 0, 8, 2, 0, 7, 0, 1, 0],
     [0, 0, 0, 0, 9, 0, 0, 0, 0],
     [0, 0, 4, 0, 3, 3, 0, 0, 0],
     [0, 0, 0, 0, 8, 0, 0, 9, 0],
     [6, 0, 0, 9, 0, 4, 1, 0, 0]]

for square_x in range(3):
    for square_y in range(3):
        square = []
        for x in range(3):
            for y in range(3):
                square.append(s[square_x * 3 + x][square_y * 3 + y])
        print(square)
