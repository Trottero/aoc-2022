import numpy as np

agg = 0

lines = []
with open ('./02/input.txt') as f:
    lines = f.readlines()

win_score = {
    'X': 0,
    'Y': 3,
    'Z': 6,
}

win_loss = {
    'X': { # Loss
        'A': 3,
        'B': 1,
        'C': 2,
    },
    'Y': { # Draw
        'A': 1,
        'B': 2,
        'C': 3,
    },
    'Z': { # Win
        'A': 2,
        'B': 3,
        'C': 1,
    },
}

lines = [tuple(line.strip().split(' ')) for line in lines]

for opp, result in lines:
    agg += win_loss[result][opp] + win_score[result]

print(agg)