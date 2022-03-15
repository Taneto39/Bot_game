def show_sudoku(matrix):
    for row in matrix:
        print(' '.join(str(num) for num in row))


def is_sudoku_filled(s):
    for row in s:
        for num in row:
            if num == 0:
                return False
    return True


def is_sudoku_correct(s):
    # row
    for row in s:
        group = []
        for num in row:
            if num != 0:
                group.append(num)
        if len(group) != len(set(group)):
            return False
    # column
    for column in range(9):
        group = []
        for row in range(9):
            if isinstance(s[row][column], int):
                if s[row][column] != 0:
                    group.append(s[row][column])
        if len(group) != len(set(group)):
            return False
    # square
    for square_x in range(3):
        for square_y in range(3):
            for x in range(3):
                group = []
                for y in range(3):
                    row = square_x * 3 + x
                    column = square_y * 3 + y
                    if isinstance(s[row][column], int):
                        if s[row][column] != 0:
                            group.append(s[row][column])
                if len(group) != len(set(group)):
                    return False
    else:
        return True


def solve_sudoku(solve, log):
    while not is_sudoku_filled(solve):
        if is_sudoku_correct(solve):
            write_try(solve, log)
        else:
            while log[-1][1] == 9:
                del log[-1]
            solve[log[-1][0][0]][log[-1][0][1]] = log[-1][1]+1
            log[-1][1] = log[-1][1]+1


def write_try(solve, log: list):
    for x, row in enumerate(solve):
        for y, blank in enumerate(row):
            if blank == 0:
                solve[x][y] = 1
                log.append([(x, y), 1])
