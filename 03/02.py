import numpy as np

agg = 0

lines = []
with open ('./03/input.txt') as f:
    lines = [line.strip() for line in f.readlines()]

def get_priority(letter): 
    if letter.isupper():
        return int(letter.lower(), 36) + 17
    return int(letter, 36) - 9

for index in range(0, len(lines), 3):
    a = lines[index]
    b = lines[index + 1]
    c = lines[index + 2]
    for chr in a:
        if chr not in b or chr not in c:
            continue
        
        prio = get_priority(chr)
        print('match:', chr, 'prio', prio)
        agg += prio
        break

    print(agg)