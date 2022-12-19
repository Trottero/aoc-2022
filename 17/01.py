import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./17/input.txt') as f:
    lines = f.readlines()[0]
    lines = [instruct for instruct in lines]

print(lines)

shapes = {
    0: [(0, 0), (1, 0), (2, 0), (3, 0)],  # Line
    1: [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)],  # Cross
    2: [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],  # L reversed
    3: [(0, 0), (0, 1), (0, 2), (0, 3)],  # Line vertical
    4: [(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
}

jet_displacement = {
    '<': -1,
    '>': 1,
}

shape_index = 0
jet_index = 0

# Just store it in an array, no one cares its small anyway
field = np.zeros((2022 * 3 + 10, 7), dtype=int)


def get_highest_true(arr):
    # Get the highest true value in the 2d array
    for y in range(arr.shape[0] - 1, -1, -1):
        if any(arr[y] == 1):
            return y
    return 0


def count_bricks(arr):
    # Count the number of bricks in the 2d array
    return np.count_nonzero(arr == 1)


def print_field(arr):
    highgest_y = get_highest_true(arr) + 5
    # Print the field
    for y in np.flip(arr[0:highgest_y], axis=0):
        for x in y:
            if x == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()

    print()


highest_y_hist = [0]
rocks_settled = 0
# Highest y value also serves as the spawn point for the new blocks
highest_y = 0
while rocks_settled < 2022:
    # Emulate a single piece falling down on the field
    piece = shapes[shape_index]
    piece_width = max([x for x, y in piece])
    current_shape_x = 2
    current_shape_y = highest_y + 3

    # print_field(field)

    settled = False
    # Simulate the shape falling down
    while not settled:
        # print(current_shape_x, current_shape_y)
        jet_disp = jet_displacement[lines[jet_index]]

        jet_index += 1
        jet_index %= len(lines)
        # Check if the jet displacement is valid with regards to bounds
        if current_shape_x + jet_disp >= 0 and current_shape_x + jet_disp + piece_width < field.shape[1]:
            collision = False
            # Check if the jet causes any of the blocks to collide with others on the field
            for x, y in piece:
                if field[current_shape_y + y, current_shape_x + x + jet_disp] == 1:
                    # collision
                    collision = True
                    break
            if not collision:
                current_shape_x += jet_disp

        # Check if moving it one down results in an out of bounds
        if current_shape_y - 1 < 0:
            settled = True
            # Place the blocks on the field
            for x, y in piece:
                field[current_shape_y + y, current_shape_x + x] = 1
            break

        # Check if the blocks collide with other blocks
        collision = False
        for x, y in piece:
            if field[current_shape_y + y - 1, current_shape_x + x] == 1:
                # collision
                collision = True
                break
        if not collision:
            current_shape_y -= 1

        else:
            # Place the blocks on the field
            for x, y in piece:
                field[current_shape_y + y, current_shape_x + x] = 1
            settled = True
    # print(current_shape_x, current_shape_y)

    rocks_settled += 1
    # Increment the shape and jet index
    shape_index += 1
    shape_index %= len(shapes)
    highest_y = get_highest_true(field) + 1
    highest_y_hist.append(highest_y)

print(highest_y)
