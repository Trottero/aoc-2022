import numpy as np

agg = 0

lines = []
with open ('./02/input.txt') as f:
    lines = f.readlines()

shape_score = {
    'X': 1,
    'Y': 2,
    'Z': 3,
}

win_loss = {
    'X': {
        'A': 3,
        'B': 0,
        'C': 6,
    },
    'Y': {
        'A': 6,
        'B': 3,
        'C': 0,
    },
    'Z': {
        'A': 0,
        'B': 6,
        'C': 3,
    },
}

lines = [tuple(line.strip().split(' ')) for line in lines]

for opp, me in lines:
    agg += win_loss[me][opp] + shape_score[me]

print(agg)