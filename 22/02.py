import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./22/input-maze.txt') as f:
    lines = [np.array([c for c in line[:-1]], dtype=str) for line in f.readlines()]

# Get longhest array in lines
max_len = max([len(line) for line in lines])

# Pad all lines to max_len
lines = np.array([np.pad(line, (0, max_len - len(line)), 'constant', constant_values=' ') for line in lines])

with open('./22/input-directions.txt') as f:
    un_processed_instructions = f.readlines()[0]
    counts = [int(c) for c in re.findall(r'\d+', un_processed_instructions)]
    turns = [c for c in re.findall(r'[LR]', un_processed_instructions)]

    instructions = []
    for i in range(len(turns)):
        instructions.append(counts[i])
        instructions.append(turns[i])
    instructions.append(counts[-1])

print(instructions)


def print_board(board):
    for line in board:
        print(''.join(line))


print_board(lines)

# overflow_map = {
#     1: (50, 0),
#     2: (100, 0),
#     3: (50, 50),
#     4: (0, 100),
#     5: (50, 100),
#     6: (0, 150),
# }

overflow_map = {
    1: (8, 0),
    2: (0, 4),
    3: (4, 4),
    4: (8, 4),
    5: (8, 8),
    6: (8, 12),
}

tile_width = 4

overflower = {
    1: {
        '+y': {
            'new_dir': '-y',
            'project': lambda x, y: (x + tile_width, tile_width - y - 1),
        },
        '-x': {
            'new_dir': '-y',
            'project': lambda x, y: (tile_width - x - 1, tile_width - y - 1),
        }
    },
}

directions = {
    '+y': (0, -1),
    '-y': (0, 1),
    '+x': (1, 0),
    '-x': (-1, 0),
}

direction_to_score = {
    '+x': 0,
    '-y': 1,
    '-x': 2,
    '+y': 3,
}

inverse_directions = {
    '+y': '-y',
    '-y': '+y',
    '+x': '-x',
    '-x': '+x',
}


rotations = {
    '+y': {
        'L': '-x',
        'R': '+x',
    },
    '-y': {
        'L': '+x',
        'R': '-x',
    },
    '+x': {
        'L': '+y',
        'R': '-y',
    },
    '-x': {
        'L': '-y',
        'R': '+y',
    },
}


def get_next_tile(board, x, y, direction):
    dx, dy = directions[direction]

    # If going out of bounds return none
    if y + dy >= len(board) or x + dx >= len(board[y]):
        return None
    if y + dy < 0 or x + dx < 0:
        return None
    if board[y + dy][x + dx] == ' ':
        return None

    return board[y + dy][x + dx]


def rotate(current_direction, turn):
    return rotations[current_direction][turn]


def move(x, y, direction):
    next_tile = get_next_tile(lines, x, y, direction)
    if next_tile is not None:
        if next_tile == '#':
            return x, y  # Do not move
        dx, dy = directions[direction]
        return x + dx, y + dy  # Process the move

    # We ran out of the board reverse direction and look until we find another none tile
    inverse_direction = inverse_directions[direction]
    dx, dy = directions[inverse_direction]

    x_temp = x
    y_temp = y

    tile = get_next_tile(lines, x_temp, y_temp, inverse_direction)
    while tile is not None:
        x_temp += dx
        y_temp += dy
        last_tile = tile
        tile = get_next_tile(lines, x_temp, y_temp, inverse_direction)

    if last_tile == '#':
        return x, y  # Do not move

    return x_temp, y_temp  # Process the move


# Find the first available tile in the first line as starting pos
x = np.argwhere(lines[0] == '.')[0][0]
y = 0
print('Starting position: ', x, y)
direction = '+x'

for instruction in instructions:
    if isinstance(instruction, int):
        for i in range(instruction):
            x, y = move(x, y, direction)
    else:
        direction = rotate(direction, instruction)

print('Final position: ', x + 1, y + 1)

password = 1000 * (y + 1) + 4 * (x + 1) + direction_to_score[direction]
print(password)
