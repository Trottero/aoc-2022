import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./23/input.txt') as f:
    lines = np.array([np.array([c for c in line.strip()]) for line in f.readlines()])

elves = np.where(lines == '#')
elves = set(zip(elves[1], len(lines) - elves[0]))


def print_elves(elves):
    minx = min(elves, key=lambda x: x[0])[0]
    maxx = max(elves, key=lambda x: x[0])[0]
    miny = min(elves, key=lambda x: x[1])[1]
    maxy = max(elves, key=lambda x: x[1])[1]
    for y in range(maxy, miny - 1, -1):
        for x in range(minx, maxx + 1):
            if (x, y) in elves:
                print('#', end='')
            else:
                print('.', end='')
        print()

    print()


print_elves(elves)

directions_checks = {
    'N': [(0, 1), (-1, 1), (1, 1)],
    'S': [(0, -1), (-1, -1), (1, -1)],
    'E': [(1, 0), (1, 1), (1, -1)],
    'W': [(-1, 0), (-1, 1), (-1, -1)],
}

apply_direction = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
}

directions_all_around = set()
for direction in directions_checks.values():
    directions_all_around.update(direction)

directions = np.array(['N', 'S', 'W', 'E'])

rounds = 1
while True:
    # Dictionary keyed by new positions and the elves that want to move there.
    proposed_directions = {}
    new_elves = []
    for elfx, elfy in elves:
        # Check if elf has another elf around it
        if not any((elfx + dx, elfy + dy) in elves for dx, dy in directions_all_around):
            # If not, continue
            new_elves.append((elfx, elfy))
            continue

        # Check in all of the directions
        valid_dir = False
        for direction in directions:
            directions_to_check = directions_checks[direction]
            # Check if there is an elf in none of the directions
            if all((elfx + dx, elfy + dy) not in elves for dx, dy in directions_to_check):
                proposed_dir = apply_direction[direction]
                proposed_position = (elfx + proposed_dir[0], elfy + proposed_dir[1])

                if proposed_position not in proposed_directions:
                    proposed_directions[proposed_position] = []

                proposed_directions[proposed_position].append((elfx, elfy))
                valid_dir = True
                break

        if not valid_dir:
            new_elves.append((elfx, elfy))

    elf_moved = False
    for new_position, old_positions in proposed_directions.items():
        if len(old_positions) == 1:
            elf_moved = True
            new_elves.append(new_position)
        else:
            # If there are more than one elf that wants to move to the same position, they will all stay put.
            new_elves.extend(old_positions)

    elves = set(new_elves)
    # print_elves(elves)

    directions = np.roll(directions, -1)

    if not elf_moved:
        print('Round where no elves moved: ', rounds)
        break
    rounds += 1

minx = min(elves, key=lambda x: x[0])[0]
maxx = max(elves, key=lambda x: x[0])[0]
miny = min(elves, key=lambda x: x[1])[1]
maxy = max(elves, key=lambda x: x[1])[1]

xsize = abs(maxx - minx) + 1
ysize = abs(maxy - miny) + 1

area = xsize * ysize
area = area - len(elves)
print(area)
