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

instruction_queue = []

signal_strength_cycles = [20, 60, 100, 140, 180, 220]
signal_strength = []

cycle = 1

for instruction_line in lines:
    instruction, *args = instruction_line.strip().split(' ')
    args = [int(arg) for arg in args]

    time_left = instruction_computation_time[instruction]

    while time_left > 0:
        time_left -= 1
        if cycle in signal_strength_cycles:
            print(f'Cycle: {cycle}, Signal strength: {register["X"]}')
            signal_strength.append((cycle) * register['X'])
        cycle += 1

    # Execute instructions that are ready
    instructions[instruction](*args)


print(signal_strength)
print(sum(signal_strength))

print(register)
