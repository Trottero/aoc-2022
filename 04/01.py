import numpy as np

agg = 0

lines = []
with open ('./04/input.txt') as f:
    lines = f.readlines()
lines = [[tuple([int(sec) for sec in seg.split('-')]) for seg in line.strip().split(',')] for line in lines]

print(lines[0])

def a_contains_b(a, b):
    a_start, a_end = a
    b_start, b_end = b
    return a_start <= b_start and a_end >= b_end

for a, b in lines:
    if a_contains_b(a, b) or a_contains_b(b, a):
        agg += 1
        continue

print(agg)