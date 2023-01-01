
with open('./25/input.txt') as f:
    lines = [reversed([c for c in line.strip()]) for line in f.readlines()]

value_map = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2,
}

decimals = []
for l in lines:
    decimal = [5 ** i * value_map[c] for i, c in enumerate(l)]
    decimals.append(sum(decimal))

decimal_sum = sum(decimals)
print(decimal_sum)


for i, d in enumerate(reversed(str(decimal_sum))):
    pass

mapmap = {
    '0': ['0'],
    '1': ['1'],
    '2': ['2'],
    '3': ['=', '1'],
    '4': ['-', '1'],
}


def to_snafu(decimal):
    snafu_num = []
    position = 0
    while decimal != 0:
        prev = 0
        if len(snafu_num) > position:
            prev = snafu_num.pop()

        # Calculate the previous overflow
        prev = int(prev) * (5 ** position)
        # Add to current
        decimal += prev

        # This is the current amount that we are solving
        to_solve = (decimal) // (5**(position))

        # We can only solve up to 5
        to_solve %= 5

        result = mapmap[str(to_solve)]

        snafu_num.extend(result)

        # Remove the amount we just solved
        decimal = decimal - (to_solve * (5**position))
        position += 1

    return "".join(reversed(snafu_num))


print(to_snafu(decimal_sum))
