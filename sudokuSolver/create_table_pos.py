txt = ['0 6 0 0 7 0 0 0 0',
       '4 0 7 3 0 0 0 0 5',
       '0 2 0 0 0 0 4 0 0',
       '2 0 0 0 0 0 0 0 0',
       '3 0 4 0 1 0 9 0 0',
       '0 0 0 0 0 9 0 0 6',
       '0 0 0 5 0 0 0 8 0',
       '9 0 1 0 3 0 6 0 0',
       '0 7 0 0 0 0 0 0 0']
table = []
for row in txt:
    table.append([int(ele) for ele in row.split(' ')])
for x, row in enumerate(table):
    for y, char in enumerate(row):
        if char != 0:
            print(f'({x},{y})={char}')
