from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./14/input.txt') as f:
    lines = [[tuple(int(i) for i in splt.split(',')) for splt in line.strip().split(' -> ')] for line in f.readlines()]


class Line():
    def __init__(self, start, end=None):
        # Create a line from a to b
        self.start = start
        if end is None:
            self.end = start
        else:
            self.end = end

    def intersects(self, pt):
        # Figure out if the line is horizontal or vertical
        if self.start[0] == self.end[0]:
            # Vertical
            return self.start[0] == pt[0] and min(self.start[1], self.end[1]) <= pt[1] <= max(self.start[1], self.end[1])
        if self.start[1] == self.end[1]:
            # Horizontal
            return self.start[1] == pt[1] and min(self.start[0], self.end[0]) <= pt[0] <= max(self.start[0], self.end[0])


segments = []

# Convert the input to line segments
for line in lines:
    for seg_ind in range(0, len(line) - 1):
        segments.append(Line(line[seg_ind], line[seg_ind + 1]))

print(f'No. of segments: {len(segments)}')

# Find the largest y coordinate in the known set of lines
max_y = max([max(seg.start[1], seg.end[1]) for seg in segments])

print(f'Highest points: {max_y}')

# Sand simulation
sand_start = (500, 0)
sand_loc = sand_start

# List of tuples of settled sand position.
sand_positions = []


def is_tile_taken(coord):
    # Return true if the tile is taken by a rock or sand
    return any([seg.intersects(coord) for seg in segments]) or coord in sand_positions


while sand_loc[1] < max_y:
    # Attempt to move the block downwards
    sand_loc_potential = (sand_loc[0], sand_loc[1] + 1)
    if not is_tile_taken(sand_loc_potential):
        sand_loc = sand_loc_potential
        continue

    # Blocked, move it to left and down
    sand_loc_potential = (sand_loc[0] - 1, sand_loc[1] + 1)
    if not is_tile_taken(sand_loc_potential):
        sand_loc = sand_loc_potential
        continue

    # Blocked, move it to right and down
    sand_loc_potential = (sand_loc[0] + 1, sand_loc[1] + 1)
    if not is_tile_taken(sand_loc_potential):
        sand_loc = sand_loc_potential
        continue

    # All blocked, this sand has settled
    sand_positions.append(sand_loc)
    sand_loc = sand_start

# Find the number of tiles that are settled
print(len(sand_positions))
