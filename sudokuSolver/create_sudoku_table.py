txt = '007800000\n' \
      '000000500\n' \
      '080060309\n' \
      '090000050\n' \
      '004003901\n' \
      '000010070\n' \
      '200004000\n' \
      '000000010\n' \
      '070030806'
table = []
print('[', end='')
for row in txt.split('\n'):
    table.append('['+', '.join([char for char in row])+']')
print(',\n'.join(table)+']')
