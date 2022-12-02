import numpy as np


lines = []
with open ('./02/input.txt') as f:
    lines = f.readlines()

opts = ["A", "B", "C"]

opts_offset = {
    "X": 2, # Loss increase with 2 indices
    "Y": 0, # Draw increase with 0 indices
    "Z": 1, # Win increase with -2 indices
}

game_results = {
    "X": 0,
    "Y": 3,
    "Z": 6,
}

lines = [tuple(line.strip().split(' ')) for line in lines]

agg = 0
for opp, result in lines:
    move_index = (opts.index(opp) + opts_offset[result]) % 3
    agg += move_index + 1 + game_results[result]

print(agg)