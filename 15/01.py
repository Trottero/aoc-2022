import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./15/input.txt') as f:
    lines = [tuple([int(x) for x in re.findall(r'\d+', line)]) for line in f.readlines()]


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

line_coords = set()

line_pos = 0

for sensor in sensors:
    fr, to = sensor.line_at_y(line_pos)
    if fr is not None:
        line_coords = line_coords.union(set(range(fr, to + 1)))

# Get all the x coordinates of the sensors on the line and remove them from the set
sensor_x_coords = set([sensor.sensor_location[0] for sensor in sensors if sensor.sensor_location[1] == line_pos])
line_coords = line_coords.difference(sensor_x_coords)

beacon_x_coords = set([sensor.closest_beacon_location[0] for sensor in sensors if sensor.closest_beacon_location[1] == line_pos])
line_coords = line_coords.difference(beacon_x_coords)

print(len(line_coords), min(line_coords), max(line_coords))
