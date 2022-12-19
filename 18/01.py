import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./18/input.txt') as f:
    lines = [tuple(int(i) for i in line.split(',')) for line in f.readlines()]


droplets = set()
agg = 0

for x, y, z in lines:
    droplets.add((x, y, z))
    # Check all 6 directions if there's a cube adjecent
    cubes_adjecent = 0
    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)):
        if (x + dx, y + dy, z + dz) in droplets:
            cubes_adjecent += 1

    # 6 - cubes_adjecent is the number of cubes that are not adjecent (free sides)
    agg += (6 - cubes_adjecent)
    agg -= cubes_adjecent  # New connections

print(agg)
