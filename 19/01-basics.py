import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./19/input.txt') as f:
    lines = [[int(match) for match in re.findall(r'\d+', line)] for line in f.readlines()]

print(lines)

type_to_yield = {
    'ore': [1, 0, 0, 0],
    'clay': [0, 1, 0, 0],
    'obsidian': [0, 0, 1, 0],
    'geode': [0, 0, 0, 1],
}


def add(a, b):
    return [aa + bb for aa, bb in zip(a, b)]


def can_build(resources, cost):
    return all(r >= c for r, c in zip(resources, cost))


def should_build(current_yield, max_reqs, bot_yield):
    for i, y in enumerate(bot_yield):
        if y == 0:
            continue
        if y == len(bot_yield) - 1:
            return True
        return current_yield[i] < max_reqs[i]


def search(current_yield, current_resources, bots, max_reqs, minutes):
    # Current_yield is a 4d vector
    # Same goes for current resources.

    # Nothing to do in the last minute, just increment the state.
    if minutes == 1:
        return add(current_resources, current_yield)[-1]

    # handle not building anything.
    nothing = search(current_yield, add(current_resources, current_yield), bots, max_reqs, minutes - 1)
    geode_count = [nothing]
    for bot_cost, bot_yield in bots:
        if can_build(current_resources, bot_cost) and should_build(current_yield, max_reqs, bot_yield):
            pass

    return max(geode_count)


minutes = 24

max_geodes = []
for id, ore_bot_cost, clay_bot_cost, obsidian_bot_cost_ore, obsidian_bot_cost_clay, geode_bot_cost_ore, geode_bot_cost_obs in lines:
    ore_bot = ([ore_bot_cost, 0, 0, 0], type_to_yield['ore'])
    clay_bot = ([clay_bot_cost, 0, 0, 0], type_to_yield['clay'])
    obsidian_bot = ([obsidian_bot_cost_ore, obsidian_bot_cost_clay, 0, 0], type_to_yield['obsidian'])
    geode_bot = ([geode_bot_cost_ore, 0, geode_bot_cost_obs, 0], type_to_yield['geode'])

    bots = [ore_bot, clay_bot, obsidian_bot, geode_bot]
    resource_costs = np.array([bot[0] for bot in bots])
    max_reqs = np.max(resource_costs, axis=0)

    max_for_blueprint = search(np.array([1, 0, 0, 0]), np.zeros(4), bots, max_reqs, minutes)
    print(max_for_blueprint)
    max_geodes.append(max_for_blueprint)
print(max_geodes)
