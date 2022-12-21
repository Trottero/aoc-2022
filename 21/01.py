import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./21/input.txt') as f:
    lines = [line.strip().split(': ') for line in f.readlines()]
    lines = {line[0]: line[1:] for line in lines}


expanded = {monkey: int(val[0]) for monkey, val in lines.items() if val[0].isdigit()}

to_remove = [monkey for monkey in expanded.keys()]
for monkey in to_remove:
    lines.pop(monkey)


op_map = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x / y
}

while len(lines.keys()) > 0:
    to_remove = []
    for monkey, val in lines.items():
        left, op, right = val[0].split(' ')
        if left in expanded and right in expanded:
            to_remove.append(monkey)
            expanded[monkey] = op_map[op](expanded[left], expanded[right])

    for monkey in to_remove:
        lines.pop(monkey)

print(expanded['root'])
