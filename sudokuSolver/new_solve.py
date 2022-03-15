from def_new import *

sudoku_table = [[0, 6, 0, 0, 0, 0, 3, 0, 0],
                [0, 7, 0, 0, 1, 0, 0, 0, 0],
                [3, 0, 1, 0, 0, 2, 0, 4, 0],
                [0, 1, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 4, 0, 0, 8],
                [9, 0, 5, 0, 2, 0, 7, 0, 0],
                [0, 0, 0, 9, 0, 0, 0, 7, 0],
                [2, 0, 3, 0, 5, 0, 9, 0, 0],
                [6, 0, 0, 0, 0, 0, 0, 0, 0]]
solve = sudoku_table.copy()
log = []  # pos, num
solve_sudoku(solve, log)
show_sudoku(solve)
