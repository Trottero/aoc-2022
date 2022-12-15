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

line_coords = set()

start_time = time.perf_counter()


def range_list_covers(range_list, x_start, x_max):
    for x in range(x_start, x_max + 1):
        covered = False
        for fr, to in range_list:
            if fr <= x <= to:
                covered = True
                break

        if not covered:
            return False, x

    return True, None


x_max = 4_000_000
y_max = 4_000_000

for y in tqdm(range(0, y_max + 1)):
    range_list = []
    for sensor in sensors:
        fr, to = sensor.line_at_y(y)
        if fr is not None:
            range_list.append((fr, to))

    covers, x2 = range_list_covers(range_list, 0, x_max)
    if not covers:
        print('success!', x2, y)
        print('result:', x2 * 4_000_000 + y)
        break

print(time.perf_counter() - start_time)
