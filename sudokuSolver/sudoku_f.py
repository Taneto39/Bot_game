def show_sudoku(matrix):
    for row in matrix:
        print(' '.join(str(num) for num in row))


def write_possible(s):
    # write possible
    for row, line in enumerate(s):
        for column, num in enumerate(line):
            if num == 0:
                s[row][column] = find_possible(row, column, s)
            else:
                s[row][column] = num


def find_possible(x, y, s):
    cant_set = set()
    # row
    for num in s[x]:
        if num != 0 and isinstance(num, int):
            cant_set.add(num)
    # column
    for row in range(9):
        if s[row][y] != 0 and isinstance(s[row][y], int):
            cant_set.add(s[row][y])
    # square
    for row in range(3):
        for column in range(3):
            if s[(x // 3) * 3 + row][(y // 3) * 3 + column] != 0 \
                    and isinstance(s[(x // 3) * 3 + row][(y // 3) * 3 + column], int):
                cant_set.add(s[(x // 3) * 3 + row][(y // 3) * 3 + column])
    can_list = [int(i) for i in range(1, 10)]
    for cant in cant_set:
        can_list.remove(cant)
    return can_list


# write surely answer by can list has only one possible
def solve_by_only_one_possible(s):
    for x in range(9):
        for y in range(9):
            if isinstance(s[x][y], list):
                if len(s[x][y]) == 1:
                    s[x][y] = s[x][y][0]
                    remove_possible(x, y, s)
                    globals()['compare'] = False


def remove_possible(x, y, s):
    # row
    for can_list in s[x]:
        if isinstance(can_list, list) and s[x][y] in can_list:
            can_list.remove(s[x][y])
    # column
    for row in range(9):
        if isinstance(s[row][y], list):
            s[row][y] = [i for i in s[row][y] if i != s[x][y]]
    # square
    for row in range(3):
        for column in range(3):
            if isinstance(s[(x // 3) * 3 + row][(y // 3) * 3 + column], list):
                s[(x // 3) * 3 + row][(y // 3) * 3 + column] = [i for i in
                                                                s[(x // 3) * 3 + row][(y // 3) * 3 + column]
                                                                if i != s[x][y]]


def solve_by_unique(solve):
    # row
    for x, row in enumerate(solve):
        unique = find_unique(row)
        if unique:
            solve[x][unique[0]] = unique[1]
            remove_possible(x, unique[0], solve)
            globals()['compare'] = False
    # column
    for y in range(9):
        column = []
        for x in range(9):
            column.append(solve[x][y])
        unique = find_unique(column)
        if unique:
            solve[unique[0]][y] = unique[1]
            remove_possible(unique[0], y, solve)
            globals()['compare'] = False
    # square
    for square_x in range(3):
        for square_y in range(3):
            square = []
            for x in range(3):
                for y in range(3):
                    square.append(solve[square_x * 3 + x][square_y * 3 + y])
            unique = find_unique(square)
            if unique:
                idx = unique[0]
                x, y = (idx // 3) + (square_x * 3), (idx % 3) + (square_y * 3)
                solve[x][y] = unique[1]
                remove_possible(x, y, solve)
                globals()['compare'] = False


# return index and unique number
def find_unique(group):
    exits = [num for num in group if isinstance(num, int)]
    possible = [num for num in range(1, 10) if num not in exits]
    for num in possible:
        index_possible = []
        for index, void in enumerate(group):
            if isinstance(void, list):
                if num in void:
                    index_possible.append(index)
        if len(index_possible) == 1:
            return index_possible[0], num


def is_sudoku_filled(s):
    for row in s:
        for num in row:
            if isinstance(num, list):
                return False
    else:
        return True


def is_sudoku_correct(s):
    # row
    for row in s:
        group = []
        for num in row:
            if isinstance(num, int):
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
            group = []
            for x in range(3):
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


def solve_by_try(try_history: list):
    global solve
    if is_sudoku_conflict(solve):
        index = try_history[-1][1]+1
        while index == try_history[-1][2]:
            del try_history[-1]
            solve = convert_to_table(try_history[-1][-1])
            index = try_history[-1][1]+1
            if len(try_history) == 1:
                break
    else:
        index = 0
    for x in range(9):
        for y in range(9):
            if isinstance(solve[x][y], list):
                if index == 0:
                    try_history.append([(x, y), index, len(solve[x][y]), convert_to_string(solve)])
                else:
                    try_history[-1][1] = index
                solve[x][y] = solve[x][y][index]
                return


def first_list(solve):
    for x in range(9):
        for y in range(9):
            if isinstance(solve[x][y], list):
                return x, y
    return False
    # global solve
    # index = 0
    # if is_sudoku_conflict(s):
    #     while (try_history[-1][1]) + 1 == try_history[-1][2]:
    #         if len(try_history) == 1:
    #             solve = convert_to_table(try_history[0][-1])
    #             x, y = try_history[0][0][0], try_history[0][0][1]
    #             s[x][y] = s[x][y][-1]
    #             remove_possible(x, y, s)
    #             del try_history[-1]
    #             return
    #         else:
    #             del try_history[-1]
    #     else:
    #         index = try_history[-1][1] + 1
    #         solve = convert_to_table(try_history[-1][-1])
    #         show_sudoku(s)
    #         print(index)
    #         show_try(try_history)
    #         show_sudoku(s)
    #         del try_history[-1]
    # ic()
    # for x, row in enumerate(s):
    #     print(x, row)
    #     for y, possible in enumerate(row):
    #         print(y, possible)
    #         if isinstance(possible, list):
    #             show_sudoku(solve)
    #             try_history.append([(x, y), index, len(possible), convert_to_string(solve)])
    #             show_sudoku(s)
    #             show_sudoku(solve)
    #             solve[x][y] = solve[x][y][index]
    #             remove_possible(x, y, s)
    #             print('tried')
    #             show_try(try_history)
    #             show_sudoku(s)
    #             return

    # index = 0
    # if is_sudoku_conflict(solve):
    #     index = (try_history[-1][1]) + 1
    #     del try_history[-1]
    #     if try_history:
    #         while index >= try_history[-1][2]:
    #             del try_history[-1]
    #             solve = convert_to_table(try_history[-1][-1])
    #             index = (try_history[-1][1]) + 1
    #             print('a' * 100)
    #         else:
    #             solve = convert_to_table(try_history[-1][-1])
    #             del try_history[-1]
    #     # solve = globals()[try_history[-1][-1]].copy()
    #     del try_history[-1]
    # for x, row in enumerate(solve):
    #     for y, possible in enumerate(row):
    #         if isinstance(possible, list):
    #             try_history.append([(x, y), index, len(possible), convert_to_string(solve)])
    #             solve[x][y] = possible[index]
    #             remove_possible(x, y, solve)
    #             return


def is_sudoku_conflict(s):
    for row in s:
        for conflict in row:
            if isinstance(conflict, list):
                if not conflict:  # if conflict(list) is empty
                    return True
    return False


def there_one_list(s):
    for row in s:
        for possible in row:
            if isinstance(possible, list):
                if len(possible) == 1:
                    return True
    else:
        return False


def convert_to_string(s):
    txt = ''
    for row in s:
        for ele in row:
            if isinstance(ele, int):
                txt += str(ele)
            else:
                for char in ele:
                    txt += str(char)
            txt += ','
        else:
            txt += 'n'
    return txt


def convert_to_table(string: str):
    table = []
    sep_line = string[:-1].split('n')
    for row in sep_line:
        new_row = []
        for s in row[:-1].split(','):
            if len(s) == 1:
                new_row.append(int(s))
            else:
                new_row.append([int(i) for i in s])
        table.append(new_row)
    return table


def show_try(try_history):
    for i in try_history:
        print(i)
