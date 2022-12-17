import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./17/input.txt') as f:
    lines = f.readlines()[0]
    lines = [instruct for instruct in lines]

print(lines)

field = np.zeros((2022 * 3, 7), dtype=bool)

