from typing import List
import numpy as np
import networkx as nx

with open('./10/input.txt') as f:
    lines = [line for line in f.readlines()]


register = {'X': 1}

instruction_computation_time = {
    'noop': 1,
    'addx': 2,
}


def addx(x):
    register['X'] = register['X'] + x


def noop():
    pass


instructions = {
    'noop': noop,
    'addx': addx,
}

cycle = 1
crt_screen = []

for instruction_line in lines:
    instruction, *args = instruction_line.strip().split(' ')
    args = [int(arg) for arg in args]

    time_left = instruction_computation_time[instruction]

    while time_left > 0:
        time_left -= 1

        # Draw on the CRT screen.
        crt_x = ((cycle - 1) % 40)
        if abs(crt_x - register['X']) < 2:
            crt_screen.append('#')
        else:
            crt_screen.append('.')
        cycle += 1

    # Execute instructions that are ready
    instructions[instruction](*args)


screen = np.array(crt_screen, dtype=str).reshape(6, 40)
for row in screen:
    print(''.join(row))
