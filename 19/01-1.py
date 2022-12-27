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
    'ore': np.array([1, 0, 0, 0]),
    'clay': np.array([0, 1, 0, 0]),
    'obsidian': np.array([0, 0, 1, 0]),
    'geode': np.array([0, 0, 0, 1]),
}


class Robot():
    def __init__(self, cost, type):
        self.cost = cost
        self.resource = type_to_yield[type]
        self.robot_type = type

    def can_build(self, resources):
        return np.all(resources >= self.cost)

    def build(self, resources):
        return resources - self.cost

    def yield_resource(self, resources):
        return resources + self.resource

    def copy(self):
        return Robot(self.cost, self.robot_type)


class State():
    def __init__(self, current_yield, resources, minutes):
        self.current_yield = current_yield
        self.resources = resources
        self.minutes_left = minutes

    def copy(self):
        return State(self.current_yield.copy(), self.resources.copy(), self.minutes_left)

    def add_yield(self, y):
        self.current_yield += y

    def can_build(self, robot: Robot):
        return np.all(self.resources >= robot.cost)

    def should_buid(self, robot: Robot, max_reqs):
        i = np.nonzero(robot.resource)[0]
        if robot.resource[-1] != 0:
            return True
        return self.current_yield[i] < max_reqs[i]

    def process(self):
        self.resources += self.current_yield
        self.minutes_left -= 1

    def __hash__(self) -> int:
        return hash((tuple(self.current_yield), tuple(self.resources), self.minutes_left))


def explore_state(state: State, bots, max_reqs):
    if state.minutes_left == 0:
        # Return geodes
        return state.resources[-1]
    if state.minutes_left == 1:
        new_state = state.copy()
        new_state.process()
        return new_state.resources[-1]

    geodes = [0]

    # Explore option where we don't do anything
    new_state = state.copy()
    new_state.process()
    geode_res = explore_state(new_state, bots, max_reqs)
    geodes.append(geode_res)

    for bot in bots:
        if state.can_build(bot) and state.should_buid(bot, max_reqs):
            new_state = state.copy()
            new_state.resources -= bot.cost
            new_state.process()
            new_state.add_yield(bot.resource)
            geode_res = explore_state(new_state, bots, max_reqs)
            geodes.append(geode_res)

    return max(geodes)


minutes = 24

max_g = []
for id, ore_bot_cost, clay_bot_cost, obsidian_bot_cost_ore, obsidian_bot_cost_clay, geode_bot_cost_ore, geode_bot_cost_obs in lines:
    ore_bot = Robot(np.array([ore_bot_cost, 0, 0, 0]), 'ore')
    clay_bot = Robot(np.array([clay_bot_cost, 0, 0, 0]), 'clay')
    obsidian_bot = Robot(np.array([obsidian_bot_cost_ore, obsidian_bot_cost_clay, 0, 0]), 'obsidian')
    geode_bot = Robot(np.array([geode_bot_cost_ore, 0, geode_bot_cost_obs, 0]), 'geode')

    current_state = State(np.array([1, 0, 0, 0]), np.array([0, 0, 0, 0]), minutes)

    bots = [ore_bot, clay_bot, obsidian_bot, geode_bot]
    resource_costs = np.array([bot.cost for bot in bots])
    max_reqs = np.max(resource_costs, axis=0)

    r = explore_state(current_state, bots, max_reqs)
    print(r)
    max_g.append(r)
print(max_g)
