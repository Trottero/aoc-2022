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


tile_width = 50

overflower_coords = {
    (50, 0): 1,
    (100, 0): 2,
    (50, 50): 3,
    (0, 100): 4,
    (50, 100): 5,
    (0, 150): 6,
}

overflower = {
    1: {  # 1
        '+y': {  # done
            'new_dir': '+x',
            'project': lambda x, y: (0,  x - 50 + 150),
        },
        '-x': {  # done
            'new_dir': '+x',
            'project': lambda x, y: (0, 149 - y),
        }
    },
    2: {  # 2
        '+y': {  # done
            'new_dir': '+y',
            'project': lambda x, y: (x - 100, 199),
        },
        '-y': {  # done
            'new_dir': '-x',
            'project': lambda x, y: (99, x - 50),
        },
        '+x': {  # done
            'new_dir': '-x',
            'project': lambda x, y: (99, 149 - y),
        }
    },
    3: {  # 3
        '-x': {  # done
            'new_dir': '-y',
            'project': lambda x, y: (y - 50, 100),
        },
        '+x': {  # done
            'new_dir': '+y',
            'project': lambda x, y: (50 + y, 49),
        }
    },
    4: {  # 4
        '-x': {  # done
            'new_dir': '+x',
            'project': lambda x, y: (50, 49 - (y - 100)),
        },
        '+y': {  # done
            'new_dir': '+x',
            'project': lambda x, y: (50, 50 + x),
        }
    },
    5: {  # 5
        '+x': {  # done
            'new_dir': '-x',
            'project': lambda x, y: (149, 49 - (y - 100)),
        },
        '-y': {  # done
            'new_dir': '-x',
            'project': lambda x, y: (49, 100 + x),
        }
    },
    6: {  # 6
        '+x': {
            'new_dir': '+y',
            'project': lambda x, y: (y - 100, 149),
        },
        '-x': {
            'new_dir': '-y',
            'project': lambda x, y: (y - 100, 0),
        },
        '-y': {
            'new_dir': '-y',
            'project': lambda x, y: (x + 100, 0),
        }
    }
}

# Test 1:
print(overflower[1]['+y']['project'](51, 0) == (0, 151) and overflower[1]['+y']['new_dir'] == '+x')
print(overflower[1]['-x']['project'](50, 5) == (0, 149 - 5) and overflower[1]['-x']['new_dir'] == '+x')

# Test 2:
print(overflower[2]['+y']['project'](101, 0) == (1, 199) and overflower[2]['+y']['new_dir'] == '+y')
print(overflower[2]['-y']['project'](101, 49) == (99, 51) and overflower[2]['-y']['new_dir'] == '-x')
print(overflower[2]['+x']['project'](149, 5) == (99, 144) and overflower[2]['+x']['new_dir'] == '-x')

# Test 3:
print(overflower[3]['-x']['project'](50, 95) == (45, 100) and overflower[3]['-x']['new_dir'] == '-y')
print(overflower[3]['+x']['project'](99, 52) == (102, 49) and overflower[3]['+x']['new_dir'] == '+y')

# test 4:
print(overflower[4]['-x']['project'](0, 100) == (50, 49) and overflower[4]['-x']['new_dir'] == '+x')
print(overflower[4]['+y']['project'](48, 100) == (50, 98) and overflower[4]['+y']['new_dir'] == '+x')

# test 5:
print(overflower[5]['+x']['project'](99, 101) == (149, 48) and overflower[5]['+x']['new_dir'] == '-x')
print(overflower[5]['-y']['project'](51, 149) == (49, 151) and overflower[5]['-y']['new_dir'] == '-x')

# test 6:
print(overflower[6]['+x']['project'](49, 151) == (51, 149) and overflower[6]['+x']['new_dir'] == '+y')
print(overflower[6]['-x']['project'](0, 199) == (99, 0) and overflower[6]['-x']['new_dir'] == '-y')
print(overflower[6]['-y']['project'](1, 199) == (101, 0) and overflower[6]['-y']['new_dir'] == '-y')

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


def find_tile_seg(x, y):
    for (xkey, ykey), value in overflower_coords.items():
        if xkey <= x < xkey + tile_width and ykey <= y < ykey + tile_width:
            return value


def move(x, y, direction):
    next_tile = get_next_tile(lines, x, y, direction)
    if next_tile is not None:
        if next_tile == '#':
            return x, y, direction  # Do not move
        dx, dy = directions[direction]
        return x + dx, y + dy, direction  # Process the move

    # Next is none, we need to wrap around the cube.
    value = find_tile_seg(x, y)
    # print('Wrapping around tile: ', x, y, direction, value)
    newx, newy = overflower[value][direction]['project'](x, y)
    new_dir = overflower[value][direction]['new_dir']

    # Dont move if we are on a wall
    if lines[newy][newx] == '#':
        return x, y, direction

    # wrapped to
    # print('Wrapped to: ', newx, newy, new_dir)
    return newx, newy, new_dir


# Find the first available tile in the first line as starting pos
x = np.argwhere(lines[0] == '.')[0][0]
y = 0
print('Starting position: ', x, y)
direction = '+x'

for instruction in instructions:
    if isinstance(instruction, int):
        for i in range(instruction):
            x, y, direction = move(x, y, direction)
    else:
        direction = rotate(direction, instruction)

print('Final position: ', x + 1, y + 1)

password = 1000 * (y + 1) + 4 * (x + 1) + direction_to_score[direction]
print(password)
