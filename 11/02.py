from typing import List
import numpy as np
import re

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
    return {'round': round, 'inspections': [monkey['total_inspections'] for monkey in monkeys.values()]}


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

# Now that we have the states from the previous 150 rounds, we start looking for an interval of rep

proposed_interval = 1
# Perhaps the period is offset, we can account for this aswell

offset = 0
while proposed_interval + offset < len(states):
    a = states[offset]
    b = states[offset + proposed_interval]
    # Compute the difference between the two states this assumes that the inspections would be linearly increasing
    diff_a_b = [b['inspections'][i] - a['inspections'][i] for i in range(len(a['inspections']))]

    c = states[offset + proposed_interval * 2]

    diff_b_c = [c['inspections'][i] - b['inspections'][i] for i in range(len(b['inspections']))]

    d = states[offset + proposed_interval * 3]

    diff_c_d = [d['inspections'][i] - c['inspections'][i] for i in range(len(c['inspections']))]

    # If the difference between the two states is the same, we have found a period
    if diff_a_b == diff_b_c and diff_b_c == diff_c_d:
        print(f'Found a period of {proposed_interval} at offset {offset}')
        break

    proposed_interval += 1
