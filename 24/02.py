import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./24/input.txt') as f:
    lines = np.array([np.array([c for c in line.strip()], dtype=str) for line in f.readlines()])

# y, x
dir_to_coord = {
    '>': (0, 1),
    '<': (0, -1),
    '^': (-1, 0),
    'v': (1, 0)
}

coord_to_dir = {
    (0, 1): '>',
    (0, -1): '<',
    (-1, 0): '^',
    (1, 0): 'v'
}


# Blizards is a list of tuples, where the first element is the y, x coordinate.
# The second element is the direction of the blizzard.
blizzards = []
for marker, direction in dir_to_coord.items():
    y, x = np.nonzero(lines == marker)
    blizzards.extend([((y, x), dir_to_coord[marker]) for y, x in zip(y, x)])
    lines[y, x] = '.'


print(blizzards)


def print_board():
    blizz_coords = [blizzard[0] for blizzard in blizzards]
    for y in range(lines.shape[0]):
        for x in range(lines.shape[1]):
            if (y, x) in blizz_coords:
                i = blizz_coords.index((y, x))
                print(coord_to_dir[blizzards[i][1]], end='')
            else:
                print(lines[y, x], end='')
        print('')


print_board()


def get_neighbours(pos):
    y, x = pos
    n = []
    if y > 0:
        n.append((y - 1, x))
    if y < len(lines) - 1:
        n.append((y + 1, x))
    if x > 0:
        n.append((y, x - 1))
    if x < len(lines[0]) - 1:
        n.append((y, x + 1))

    return n

    # Find starting position.
starting_pos = (0, list(lines[0]).index('.'))
target_pos = (lines.shape[0] - 1, list(lines[-1]).index('.'))


def find_path(starting_pos, target_pos, blizzards):
    print(f'Starting position: {starting_pos}', f'Target position: {target_pos}')
    iterations = 0
    open_list = [starting_pos]
    while len(open_list) > 0:
        add_to_open = []
        for pos in open_list:
            if pos == target_pos:
                print(f'From: {pos} Found path! after {iterations}')
                return iterations, blizzards
            # Find all possible moves from this position
            neig = get_neighbours(pos)
            for n in neig:
                if n not in open_list and lines[n] != '#' and n not in add_to_open:
                    add_to_open.append(n)

        open_list.extend(add_to_open)

        # Advance all of the blizzards forward
        new_blizzards = []
        for i, ((blizzy, blizzx), (dy, dx)) in enumerate(blizzards):
            # Roll out of bounds blizzards
            if blizzy + dy >= len(lines) - 1:  # out of bounds
                blizzy = 0
            if blizzy + dy < 1:  # out of bounds
                blizzy = len(lines) - 1
            if blizzx + dx >= len(lines[0]) - 1:  # out of bounds
                blizzx = 0
            if blizzx + dx < 1:  # out of bounds
                blizzx = len(lines[0]) - 1

            new_blizzards.append(((blizzy + dy, blizzx + dx), (dy, dx)))

        blizzards = new_blizzards

        # Prune all open_list positions which overlap with a blizzard
        blizz_coords = [blizzard[0] for blizzard in blizzards]
        open_list = [pos for pos in open_list if pos not in blizz_coords]

        # print_board()
        iterations += 1


first, blizzards = find_path(starting_pos, target_pos, blizzards)
second, blizzards = find_path(target_pos, starting_pos, blizzards)
third, blizzards = find_path(starting_pos, target_pos, blizzards)
print(first, second, third)
print(first + second + third)
