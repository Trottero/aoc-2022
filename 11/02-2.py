import math
from typing import List
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re
import pandas as pd

with open('./11/input.txt') as f:
    lines = [line for line in f.readlines()]

monkeys = {}


def monkey_test(monkey, item):
    return monkey['when_true'] if item % monkey['divisibleby'] == 0 else monkey['when_false']


def monkey_operation(monkey, item):
    var1, op, var2 = monkey['operation']
    if var1 == 'old':
        var1 = item
    if var2 == 'old':
        var2 = item

    if op == '+':
        return int(var1) + int(var2)
    if op == '-':
        return int(var1) - int(var2)
    if op == '*':
        return int(var1) * int(var2)
    if op == '/':
        return int(var1) / int(var2)


def monkey_post_operation(item):
    return int(item / 3)


# Parse the monkey program
for i in range(0, len(lines), 7):
    # Extract the monkey's id
    monkey_id = int(re.findall(r'\d+', lines[i])[0])
    # Extract the monkey's starting items
    items = [int(x) for x in re.findall(r'\d+', lines[i+1])]

    operation_str = lines[i+2].split(':')[1].strip().strip('new = ').split(' ')

    # test = lines[i+3].split(':')[1].strip().split(' ')
    divisibleby = int(re.findall(r'\d+', lines[i+3])[0])
    when_true = int(re.findall(r'\d+', lines[i+4])[0])
    when_false = int(re.findall(r'\d+', lines[i+5])[0])

    monkeys[monkey_id] = {
        'items': items,
        'operation': operation_str,
        'when_true': when_true,
        'when_false': when_false,
        'divisibleby': divisibleby,
        'total_inspections': 0,
    }


def get_state(monkeys, round):
    return {
        'round': round,
        'inspections_sum': sum([monkey['total_inspections'] for monkey in monkeys.values()]),
        'inspections': [monkey['total_inspections'] for monkey in monkeys.values()]}


states = []

# The pattern is probably looping somewhere, we gotta find that loop.
# Program seems to lag after 150 rounds, so lets just do 150 rounds
for round in range(150):
    # Run the monkey program
    for key, monkey in monkeys.items():
        # For every item in the monkey's inventory
        for item in monkey['items']:
            # Perform operation
            monkey_op = monkey_operation(monkey, item)

            # Test the result
            monkey_test_result = monkey_test(monkey, monkey_op)

            # append to said monkey's inventory
            monkeys[monkey_test_result]['items'].append(monkey_op)

        monkeys[key]['total_inspections'] += len(monkey['items'])

        # Clear this monkeys inventory
        monkeys[key]['items'] = []

    # Collect the state
    state = get_state(monkeys, round + 1)
    states.append(state)

# Plot the results
sns.lineplot(x='round', y='inspections_sum', data=pd.DataFrame(states))
plt.show()
# For every monkey plot its inspections
for i in range(len(states[0]['inspections'])):
    sns.lineplot(x=list(range(150)), y=[state['inspections'][i] for state in states], label=i)
plt.show()

# For every monkey find the coefficient of its inspections
inspection_coefficients = []
no_monkeys = len(monkeys.keys())


def find_coefficient(monkey_id):
    pta = 10
    ptb = 130
    ptdiff = ptb - pta

    inspection_diff = states[ptb - 1]['inspections'][monkey_id] - states[pta - 1]['inspections'][monkey_id]
    inspection_coeff = inspection_diff / float(ptdiff)

    return inspection_coeff


for i in range(no_monkeys):
    inspection_coefficients.append(find_coefficient(i))

# Find highest 2 coefficients
highest = sorted(inspection_coefficients, reverse=True)[:2]
print(highest)
print(10_000 * math.ceil(highest[0]) * 10_000 * math.ceil(highest[1]))

# pta = 10
# ptb = 140
# ptdiff = ptb - pta

# inspection_diff = states[ptb]['inspections'] - states[pta]['inspections']
# inspection_coeff = inspection_diff / float(ptdiff)

# print(10_000 * inspection_coeff)
