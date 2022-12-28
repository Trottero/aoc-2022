import re
import time
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast
import tqdm

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


def add_remove(a, b, r):
    return [aa + bb - rr for aa, bb, rr in zip(a, b, r)]


def remove(resources, costs):
    return [aa - bb for aa, bb in zip(resources, costs)]


def can_build(resources, cost):
    return all(r >= c for r, c in zip(resources, cost))


def should_build(current_yield, max_reqs, bot_type):
    if bot_type == 'geode':
        return True
    if bot_type == 'ore':
        return current_yield[0] < max_reqs[0]
    if bot_type == 'clay':
        return current_yield[1] < max_reqs[1]
    if bot_type == 'obsidian':
        return current_yield[2] < max_reqs[2]
    else:
        raise ValueError('Unknown bot type')


def has_potential(current_resources, current_yield, max_so_far, time_left):
    # Lets say that we have enough resources to build a bot for every minute left.
    max_potential = sum([i + 1 for i in range(time_left)])
    max_potential += current_resources[-1]
    max_potential += current_yield[-1] * time_left
    return max_potential > max_so_far


global time_start
time_start = 0

global max_per_solution
max_per_solution = 5

global max_so_far
max_so_far = -1


def search(current_yield, current_resources, bots, max_reqs, minutes):
    global max_so_far
    global time_start
    global max_per_solution

    if time.time() - time_start > max_per_solution:
        return max_so_far

    # Current_yield is a 4d vector
    # Same goes for current resources.

    # Nothing to do in the last minute, just increment the state.
    if minutes == 1:
        return add(current_resources, current_yield)[-1]

    if not has_potential(current_resources, current_yield, max_so_far, minutes):
        return -1
    geode_count = []

    for bot_cost, bot_yield, bot_type in bots:
        if should_build(current_yield, max_reqs, bot_type) and can_build(current_resources, bot_cost):
            geodes = search(
                add(current_yield, bot_yield),
                add_remove(current_resources, current_yield, bot_cost),
                bots, max_reqs, minutes - 1)
            if geodes > max_so_far:
                max_so_far = geodes

            geode_count.append(geodes)

    nothing = search(current_yield, add(current_resources, current_yield), bots, max_reqs, minutes - 1)
    geode_count.append(nothing)

    return max(geode_count)


minutes = 24

max_geodes = []
for id, ore_bot_cost, clay_bot_cost, obsidian_bot_cost_ore, obsidian_bot_cost_clay, geode_bot_cost_ore, geode_bot_cost_obs in tqdm.tqdm(
        lines):
    ore_bot = ([ore_bot_cost, 0, 0, 0], type_to_yield['ore'], 'ore')
    clay_bot = ([clay_bot_cost, 0, 0, 0], type_to_yield['clay'], 'clay')
    obsidian_bot = ([obsidian_bot_cost_ore, obsidian_bot_cost_clay, 0, 0], type_to_yield['obsidian'], 'obsidian')
    geode_bot = ([geode_bot_cost_ore, 0, geode_bot_cost_obs, 0], type_to_yield['geode'], 'geode')

    bots = [ore_bot, clay_bot, obsidian_bot, geode_bot]
    resource_costs = np.array([bot[0] for bot in bots])
    max_reqs = [max(ore_bot_cost, clay_bot_cost, obsidian_bot_cost_ore, geode_bot_cost_ore), obsidian_bot_cost_clay, geode_bot_cost_obs]

    time_start = time.time()
    max_so_far = -1

    max_for_blueprint = search([1, 0, 0, 0], [0, 0, 0, 0], bots, max_reqs, minutes)
    max_geodes.append(max_for_blueprint)

print(max_geodes)
quality_levels = [geode * (i + 1) for i, geode in enumerate(max_geodes)]
print('Quality levels: ', quality_levels)
print('Sum of quality levels: ', sum(quality_levels))
