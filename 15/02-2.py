import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast
import time
from tqdm import tqdm

with open('./15/input.txt') as f:
    lines = [tuple([int(x) for x in re.findall("[-+]?[\d]+", line)]) for line in f.readlines()]


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Sensor():
    def __init__(self, loc, closest_beacon):
        self.sensor_location = loc
        self.closest_beacon_location = closest_beacon
        self.beacon_distance = manhattan_distance(self.sensor_location, self.closest_beacon_location)

    def line_at_y(self, y):
        # Check if the line is even out of range
        distance_to_line = abs(self.sensor_location[1] - y)
        if self.beacon_distance < distance_to_line:
            return None, None

        # Find the x coordinate of the line
        # The line is centered around the x of the location of the sensor
        # Max width is 2 *  assuming the sensor is at the center of the line
        width = 2 * (self.beacon_distance - distance_to_line)

        return self.sensor_location[0] - width // 2, self.sensor_location[0] + width // 2


sensors = [Sensor((data[0], data[1]), (data[2], data[3])) for data in lines]

start_time = time.perf_counter()

x_max = 4_000_000
y_max = 4_000_000

found = False
for y in tqdm(range(0, y_max + 1)):
    for x in range(0, x_max + 1):

        invalidates = False
        # Check if the proposed location is closer to any of the sensors than its beacon
        for sensor in sensors:
            if manhattan_distance((x, y), sensor.sensor_location) <= sensor.beacon_distance:
                invalidates = True
                break

        if not invalidates:
            print(f'({x}, {y}) is not closer to any sensor than its beacon')

print(time.perf_counter() - start_time)
