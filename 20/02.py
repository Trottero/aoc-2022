import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./20/input.txt') as f:
    lines = [int(line) for line in f.readlines()]

indexes = [(i, line * 811589153) for i, line in enumerate(lines)]

encrypted_file = [val for val in indexes]
for i in range(10):
    for original_i, value in indexes:
        index_in_encrypted = encrypted_file.index((original_i, value))
        new_index = (index_in_encrypted + value) % (len(indexes) - 1)
        encrypted_file.remove((original_i, value))
        if new_index == 0:
            encrypted_file.append((original_i, value))
        else:
            encrypted_file.insert(new_index, (original_i, value))

print(encrypted_file)

encrypted_file = [val for orig, val in encrypted_file]
print(encrypted_file)

relevant = [1000, 2000, 3000]
agg = 0
zeor_index = encrypted_file.index(0)
for ind in relevant:
    number = encrypted_file[(ind + zeor_index) % len(encrypted_file)]
    print(number)
    agg += number

print(agg)
