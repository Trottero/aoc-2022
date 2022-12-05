import numpy as np

agg = 0

lines = []
with open ('./05/input.txt') as f:
    lines = [line for line in f.readlines()]

def parse_crate_line(line):
    crates = []

    if '[' not in line:
        return [None] * 9

    for i in range(0, len(line), 4):
        selection = line[i:i+3]
        # Check empty line
        if selection == '   ':
            crates.append(None)
            continue

        # parse crate by removing [ and ]
        crates.append(selection[1:-1])

    return crates

crates = {i: [] for i in range(1, 10)}
parsing_crate = True
for ind, line in enumerate(lines):
    if line == '':
        continue

    if parsing_crate:
        line_crates = parse_crate_line(line)
        if all([crate == None for crate in line_crates]):
            parsing_crate = False
            break
        for i, crate in enumerate(line_crates):
            if crate != None:
                crates[i + 1].insert(0, crate)

print(crates, ind)

# Parse the rest of the lines
for line in lines[ind + 2:]:
    line = line.strip()
    # Get list of numbers in the line
    digits = [int(num) for num in line.split(' ') if num.isdigit()]

    amount, fr, to = digits
    # Move crates
    move = crates[fr][-amount:]
    crates[fr] = crates[fr][:-amount]
    crates[to].extend(move)

# Get the top crate for every stack
top_crates = [stack[-1] for stack in crates.values()]
print("".join(top_crates))
