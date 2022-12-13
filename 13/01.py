from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./13/input.txt') as f:
    lines = [line.strip() for line in f.readlines()]

pairs = zip([ast.literal_eval(lines[line]) for line in range(0, len(lines), 3)],
            [ast.literal_eval(lines[line]) for line in range(1, len(lines), 3)])


def compare(l, r, level=0):
    print("-" * level, l, r)
    if type(l) == int and type(r) == int:
        return l <= r

    if type(l) == int:
        return compare([l], r, level + 1)

    if type(r) == int:
        return compare(l, [r], level + 1)

    if type(l) == list and type(r) == list:
        # We now know that left is smaller or equal than right and thus can safely iterate over left
        # compare all elements in list

        # return all([compare(l[i], r[i], level + 1) for i in range(len(l))])
        for i in range(len(l)):
            if not compare(l[i], r[i], level + 1):
                return False

    raise Exception("Unknown type combination")


pairs_in_order = []
for l, r in pairs:
    # pairs_in_order.append(compare(l, r))
    print(l, r, compare(l, r))

pair_inds = []
for i, inorder in enumerate(pairs_in_order):
    if inorder:
        pair_inds.append(i + 1)

print(sum(pair_inds))
