from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast
from functools import cmp_to_key

with open('./13/input.txt') as f:
    lines = [line.strip() for line in f.readlines()]

packets = [ast.literal_eval(line) for line in lines if line != '']
packets.append([[2]])
packets.append([[6]])


def compare(l, r, level=0):
    # print("-" * level, l, r)
    if type(l) == int and type(r) == int:
        if l == r:
            return None
        return l < r

    if type(l) == int:
        return compare([l], r, level + 1)

    if type(r) == int:
        return compare(l, [r], level + 1)

    if type(l) == list and type(r) == list:
        # We now know that left is smaller or equal than right and thus can safely iterate over left
        # compare all elements in list

        # return all([compare(l[i], r[i], level + 1) for i in range(len(l))])
        for i in range(len(l)):
            # If we exhuast the right before the left, then wrong order.
            if i >= len(r):
                return False

            # Else compare left and right element
            cmp = compare(l[i], r[i], level + 1)
            # Check if the result is conclusive
            if cmp is not None:
                # If it is, return it.
                return cmp

        if len(l) == len(r):
            # Non conclusive, so return None
            return None
        return len(l) < len(r)

    raise Exception("Unknown type combination")


def comp_to_num(a, b):
    comp = compare(a, b)
    if comp is None:
        return 0
    if comp:
        return -1
    return 1


compare_key = cmp_to_key(comp_to_num)

packets.sort(key=compare_key)
for packet in packets:
    print(packet)

print((packets.index([[2]]) + 1)*(packets.index([[6]]) + 1))
