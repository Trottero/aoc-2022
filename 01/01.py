import numpy as np

agg = 0
max_agg = 0
with open ('./01/input.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n':
            if agg > max_agg:
                max_agg = agg
            agg = 0
            continue
        agg += int(line)

print(max_agg)