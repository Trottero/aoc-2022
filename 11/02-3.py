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


def monkey_post_operation(item, worrylevelsmult):
    return item % worrylevelsmult


worrylevelsmult = 1

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

    worrylevelsmult *= divisibleby

    monkeys[monkey_id] = {
        'items': items,
        'operation': operation_str,
        'when_true': when_true,
        'when_false': when_false,
        'divisibleby': divisibleby,
        'total_inspections': 0,
    }

for roun in range(10000):
    # Run the monkey program
    for key, monkey in monkeys.items():
        # For every item in the monkey's inventory
        for item in monkey['items']:
            # Perform operation
            monkey_op = monkey_operation(monkey, item)
            monkey_op = monkey_post_operation(monkey_op, worrylevelsmult)
            # Test the result
            monkey_test_result = monkey_test(monkey, monkey_op)

            # append to said monkey's inventory
            monkeys[monkey_test_result]['items'].append(monkey_op)

        monkeys[key]['total_inspections'] += len(monkey['items'])

        # Clear this monkeys inventory
        monkeys[key]['items'] = []


# find two monkeys with highest total inspections
sorted_monkeys = sorted(monkeys.items(), key=lambda x: x[1]['total_inspections'], reverse=True)
top2 = [x[1]['total_inspections'] for x in sorted_monkeys[:2]]
print(top2[0] * top2[1])
