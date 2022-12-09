from typing import List
import numpy as np
import networkx as nx

with open('./09/input.txt') as f:
    lines = [[line.strip().split(' ')[0]] * int(line.strip().split(' ')[1]) for line in f.readlines()]
    lines = [item for sublist in lines for item in sublist]

head = (0, 0)
tail = (0, 0)


apply_direction = {
    'U': lambda x: (x[0], x[1] + 1),
    'D': lambda x: (x[0], x[1] - 1),
    'L': lambda x: (x[0] - 1, x[1]),
    'R': lambda x: (x[0] + 1, x[1])
}

angle_to_direction = {
    0: ['U'],
    45: ['U', 'R'],
    90: ['R'],
    135: ['D', 'R'],
    180: ['D'],
    -45: ['U', 'L'],
    -90: ['L'],
    -135: ['D', 'L'],
}


def tail_is_valid(head, tail):
    # Check if the tail is too far away using euclidean distance
    return not np.linalg.norm(np.array(head) - np.array(tail)) > (np.sqrt(2) + 0.001)


def move(head, tail):
    if tail_is_valid(head, tail):
        return tail

    # Else we have to move it in a diagonal direction to the head
    # Get the angle between the tail and the head
    angle = np.rad2deg(np.arctan2(head[0] - tail[0], head[1] - tail[1]))
    # Find the closest angle in the angle_to_direction dict
    closest_angle = min(angle_to_direction.keys(), key=lambda x: abs(x - angle))

    # print(f'Angle: {angle}, Closest angle: {closest_angle}')
    # Move the tail in the direction of the closest angle

    new_tail = tail
    for moves in angle_to_direction[closest_angle]:
        new_tail = apply_direction[moves](new_tail)

    return new_tail


def print_grid(headpos, tailpos):
    grid = np.zeros((10, 10), dtype=str)
    grid[:, :] = '.'
    grid[tuple(reversed(tailpos))] = 'T'
    grid[tuple(reversed(headpos))] = 'H'

    print(grid)


positions = set()

# print_grid(head, tail)

knots = [(0, 0)] * 10

for direction in lines:
    # Move the head first
    knots[0] = apply_direction[direction](knots[0])

    for i in range(1, len(knots)):
        knots[i] = move(knots[i-1], knots[i])
    # print(f'Head: {head}, Tail: {tail}')
    # print_grid(head, tail)

    positions.add(knots[-1])

print(len(positions))
