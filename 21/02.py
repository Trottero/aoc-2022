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

expanded.pop('humn')

op_map = {
    '+': lambda x, y: x + y,
    '*': lambda x, y: x * y,
    '-': lambda x, y: x - y,
    '/': lambda x, y: x / y
}

inverse_op_map_right = {
    '+': lambda left, expected: expected - left,
    '-': lambda left, expected: left - expected,
    '*': lambda left, expected: expected / left,
    '/': lambda left, expected: left / expected
}

inverse_op_map_left = {
    '+': lambda right, expected: expected - right,
    '-': lambda right, expected: right + expected,
    '*': lambda right, expected: expected / right,
    '/': lambda right, expected: expected * right
}

while len(lines.keys()) > 0:
    to_remove = []
    for monkey, val in lines.items():
        left, op, right = val[0].split(' ')
        if left in expanded and right in expanded:
            to_remove.append(monkey)
            expanded[monkey] = op_map[op](expanded[left], expanded[right])

    if len(to_remove) == 0:
        print('Could not resolve')
        break

    for monkey in to_remove:
        lines.pop(monkey)

left, op, right = lines['root'][0].split(' ')

if left in expanded:
    eq = expanded[left]
    side = right
else:
    eq = expanded[right]
    side = left

print(lines)

print(f'Side: {side} should be {eq}')


def solve(current, should_result_in):
    # Traverse the tree untill we encounter humn
    left, op, right = lines[current][0].split(' ')
    if left == 'humn':
        return inverse_op_map_left[op](expanded[right], should_result_in)
    elif right == 'humn':
        return inverse_op_map_right[op](expanded[left], should_result_in)

    if left in expanded:
        # same as humn right
        return solve(right, inverse_op_map_right[op](expanded[left], should_result_in))
    # same as humn left
    return solve(left, inverse_op_map_left[op](expanded[right], should_result_in))


print(solve(side, eq))
