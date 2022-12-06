import numpy as np

agg = 0

marker = []
with open ('./06/input.txt') as f:
    line = [line.strip() for line in f.readlines()][0]

marker_len = 14
for i, c in enumerate(line):
    marker = line[i:i+marker_len]
    if len(set(marker)) == len(marker):
        print(i + marker_len)
        break 