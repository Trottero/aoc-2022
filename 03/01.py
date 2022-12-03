import numpy as np

agg = 0

lines = []
with open ('./03/input.txt') as f:
    lines = f.readlines()

def get_priority(letter): 
    if letter.isupper():
        return int(letter.lower(), 36) + 17
    return int(letter, 36) - 9

for line in lines:
    line = line.strip()
    a = line[:int(len(line) / 2)]
    b = line[int(len(line) / 2):]
    print(a, '-', b)

    for c in a:
        if c not in b:
            continue
        
        prio = get_priority(c)
        print('match:', c, 'prio', prio)
        agg += prio
        break

print(agg)