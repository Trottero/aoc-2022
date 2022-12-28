import re
import time
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast
import tqdm

with open('./19/input.txt') as f:
    lines = [[int(match) for match in re.findall(r'\d+', line)] for line in f.readlines()][:3]

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
    if bot_type == 'ore':
        return current_yield[0] <= max_reqs[0]
    if bot_type == 'clay':
        return current_yield[1] <= max_reqs[1]
    if bot_type == 'obsidian':
        return current_yield[2] <= max_reqs[2]
    if bot_type == 'geode':
        return True
    else:
        raise ValueError('Unknown bot type')


def is_ever_possible_to_build(current_yield, current_resources, bot_type, bot_cost, minutes_left):
    if bot_type == 'ore':
        return (current_yield[0] * minutes_left + current_resources[0]) >= bot_cost[0]
    if bot_type == 'clay':
        return (current_yield[0] * minutes_left + current_resources[0]) >= bot_cost[0]
    if bot_type == 'obsidian':
        return (current_yield[0] * minutes_left + current_resources[0]) >= bot_cost[0] and (current_yield[1] * minutes_left + current_resources[1]) >= bot_cost[1]
    if bot_type == 'geode':
        return (current_yield[0] * minutes_left + current_resources[0]) >= bot_cost[0] and (current_yield[2] * minutes_left + current_resources[2]) >= bot_cost[2]
    else:
        raise ValueError('Unknown bot type')


def has_potential(current_resources, current_yield, max_so_far, time_left):
    # Lets say that we have enough resources to build a bot for every minute left.
    max_potential = sum([i + 1 for i in range(time_left - 1)])
    max_potential += current_resources[-1]
    max_potential += current_yield[-1] * time_left
    return max_potential > max_so_far


global max_so_far
max_so_far = -1


def search(current_yield, current_resources, bots, max_reqs, minutes):
    global max_so_far

    # Current_yield is a 4d vector
    # Same goes for current resources.

    # Nothing to do in the last minute, just increment the state.
    if minutes == 1:
        return add(current_resources, current_yield)[-1]

    if not has_potential(current_resources, current_yield, max_so_far, minutes):
        return -1

    geode_count = []

    for bot_cost, bot_yield, bot_type in bots:
        if should_build(
                current_yield, max_reqs, bot_type) and is_ever_possible_to_build(
                current_yield, current_resources, bot_type, bot_cost, minutes - 1):

            # Fast forward time untill we can actually build this robot.
            new_resources = current_resources.copy()
            b_min = minutes

            # Decrease untill we can build the bot.
            while not can_build(new_resources, bot_cost):
                new_resources = add(new_resources, current_yield)
                b_min -= 1

            # We should now be at a state where we can build the bot at the start of the turn.
            # Start building the bot
            new_resources = remove(new_resources, bot_cost)

            # Increment the state.
            new_resources = add(new_resources, current_yield)
            b_min -= 1

            # Bot has finished building, add it to the list of bots.
            new_yield = add(current_yield, bot_yield)

            geodes = search(
                new_yield,
                new_resources,
                bots, max_reqs, b_min)

            if geodes > max_so_far:
                max_so_far = geodes

            geode_count.append(geodes)

    # Not able to build any bots, just increment the state.
    if len(geode_count) == 0:
        new_resources = current_resources.copy()
        while minutes > 0:
            new_resources = add(new_resources, current_yield)
            minutes -= 1
        return new_resources[-1]

    return max(geode_count)


minutes = 32

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

    max_so_far = -1

    max_for_blueprint = search([1, 0, 0, 0], [0, 0, 0, 0], bots, max_reqs, minutes)
    max_geodes.append((id, max_for_blueprint))

print('No of geodes:', max_geodes)
quality_levels = [geode * i for i, geode in max_geodes]
print('Quality levels: ', quality_levels)
print('Sum of quality levels: ', sum(quality_levels))

mult = 1
for id, geodes in max_geodes:
    mult *= geodes

print('Mult: ', mult)
