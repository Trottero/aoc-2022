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


minutes = 24

for id, ore_bot_cost, clay_bot_cost, obsidian_bot_cost_ore, obsidian_bot_cost_clay, geode_bot_cost_ore, geode_bot_cost_obs in lines:
    ore_bot = Robot(np.array([ore_bot_cost, 0, 0, 0]), 'ore')
    clay_bot = Robot(np.array([clay_bot_cost, 0, 0, 0]), 'clay')
    obsidian_bot = Robot(np.array([obsidian_bot_cost_ore, obsidian_bot_cost_clay, 0, 0]), 'obsidian')
    geode_bot = Robot(np.array([geode_bot_cost_ore, 0, geode_bot_cost_obs, 0]), 'geode')

    currently_building = None
    active_robots = [ore_bot.copy()]
    resources = np.array([0, 0, 0, 0])

    for _ in range(minutes):
        # Find optimal robot to build
        if currently_building is None:
            for robot in [geode_bot, obsidian_bot, clay_bot, ore_bot]:
                if robot.can_build(resources):
                    currently_building = robot
                    resources = robot.build(resources)
                    break

        # Increment resources
        for robot in active_robots:
            resources = robot.yield_resource(resources)

        # Finish building robot
        if currently_building is not None:
            active_robots.append(currently_building.copy())
            currently_building = None

    # Get the number of geodes
    print(resources)
    print(id * resources[-1])
