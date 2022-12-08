from typing import List
import numpy as np
import networkx as nx

with open ('./08/input.txt') as f:
    lines = np.array([np.array([int(n) for n in line.strip()]) for line in f.readlines()])

def sweep(area, direction):
    y_size, x_size = area.shape

    visible_pixels = np.zeros(area.shape, dtype=int)

    if direction == 'left':
        max_slice = np.array([-1] * y_size)
        for x in range(x_size):
            tree_slice = area[:, x]
            visible_pixels[:, x] = tree_slice > max_slice

            max_slice = np.maximum(max_slice, tree_slice)

        return visible_pixels

    if direction == 'right':
        max_slice = np.array([-1] * y_size)
        for x in reversed(range(x_size)):
            tree_slice = area[:, x]
            visible_pixels[:, x] = tree_slice > max_slice

            max_slice = np.maximum(max_slice, tree_slice)

        return visible_pixels

    if direction == 'up':
        max_slice = np.array([-1] * x_size)
        for y in range(y_size):
            tree_slice = area[y, :]
            visible_pixels[y, :] = tree_slice > max_slice

            max_slice = np.maximum(max_slice, tree_slice)

        return visible_pixels
    
    if direction == 'down':
        max_slice = np.array([-1] * x_size)
        for y in reversed(range(y_size)):
            tree_slice = area[y, :]
            visible_pixels[y, :] = tree_slice > max_slice

            max_slice = np.maximum(max_slice, tree_slice)

        return visible_pixels

# Sweep over lines matrix from left to right
# Reminder that the the lines are y,x indexed
visible_pixels = np.zeros(lines.shape, dtype=int)

directions = ['left', 'right', 'up', 'down']
for direction in directions:
    visible_pixels += sweep(lines, direction)

print(np.count_nonzero(visible_pixels))