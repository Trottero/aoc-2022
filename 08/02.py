from typing import List
import numpy as np
import networkx as nx

with open ('./08/input.txt') as f:
    lines = np.array([np.array([int(n) for n in line.strip()]) for line in f.readlines()])

def calculate_scenic_score(area, pt):
    # The scenic score is the amount of trees that are visible from the point
    # The point is a tuple of (y, x)
    y_size, x_size = area.shape
    
    pt_height = area[pt]

    scores = {
        '+x': 0,
        '-x': 0,
        '+y': 0,
        '-y': 0,
    }

    # Get number of trees visible from the point when going in positive x direction
    x = pt[1] + 1
    maxx = -1
    while x < x_size and pt_height > maxx:
        scores['+x'] += 1
        tr_height = area[pt[0], x]
        maxx = max(maxx, tr_height)
        x += 1

    # Get number of trees visible from the point when going in negative x direction
    x = pt[1] - 1
    maxx = -1
    while x >= 0 and pt_height > maxx:
        scores['-x'] += 1
        tr_height = area[pt[0], x]
        maxx = max(maxx, tr_height)
        x -= 1

    # Get number of trees visible from the point when going in positive y direction
    y = pt[0] + 1
    maxy = -1
    while y < y_size and pt_height > maxy:
        scores['+y'] += 1
        tr_height = area[y, pt[1]]
        maxy = max(maxy, tr_height)
        y += 1
    
    # Get number of trees visible from the point when going in negative y direction
    y = pt[0] - 1
    maxy = -1
    while y >= 0 and pt_height > maxy:
        scores['-y'] += 1
        tr_height = area[y, pt[1]]
        maxy = max(maxy, tr_height)
        y -= 1
    
    return scores['+x'] * scores['-x'] * scores['+y'] * scores['-y']



# Get the point with the highest scenic score
max_score = 0
max_pt = None
for y in range(lines.shape[0]):
    for x in range(lines.shape[1]):
        score = calculate_scenic_score(lines, (y, x))
        if score > max_score:
            max_score = score
            max_pt = (y, x)


print(max_pt)
print(max_score)