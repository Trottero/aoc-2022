import numpy as np

large_vals = []
agg = 0
with open ('./01/input.txt') as f:
    while True:
        line = f.readline()
        if not line:
            break
        if line == '\n':
            large_vals.append(agg)
            large_vals = sorted(large_vals, reverse=True)[:3]
            agg = 0
            continue
        agg += int(line)

print(large_vals)
print(sum(large_vals))