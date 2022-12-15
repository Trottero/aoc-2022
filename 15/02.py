import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast
import time
from tqdm import tqdm
from shapely import Polygon, MultiPolygon, Point
from shapely.ops import unary_union
from shapely.plotting import plot_polygon, plot_points


with open('./15/input.txt') as f:
    lines = [tuple([int(x) for x in re.findall("[-+]?[\d]+", line)]) for line in f.readlines()]


def manhattan_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


class Sensor():
    def __init__(self, loc, closest_beacon):
        self.sensor_location = loc
        self.closest_beacon_location = closest_beacon
        self.beacon_distance = manhattan_distance(self.sensor_location, self.closest_beacon_location)

    def as_polygon(self) -> Polygon:
        polygon_locations = []
        polygon_locations.append((self.sensor_location[0], self.sensor_location[1] - self.beacon_distance))
        polygon_locations.append((self.sensor_location[0] + self.beacon_distance, self.sensor_location[1]))
        polygon_locations.append((self.sensor_location[0], self.sensor_location[1] + self.beacon_distance))
        polygon_locations.append((self.sensor_location[0] - self.beacon_distance, self.sensor_location[1]))
        return Polygon(polygon_locations)

    def beacon_poly(self) -> Point:
        return Point(self.closest_beacon_location)

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


polygons = [sensor.as_polygon().buffer(0) for sensor in sensors]
# beacon_polys = [sensor.beacon_poly().buffer(0) for sensor in sensors]

# polygons.extend(beacon_polys)

# # plot a single polygon
# for poly in polygons:
#     plot_polygon(poly)

# plt.gca().invert_yaxis()
# plt.show()

x_max = 4_000_000
y_max = 4_000_000


combined_poly: MultiPolygon = unary_union(polygons)

# plot_polygon(combined_poly)
# plt.gca().invert_yaxis()
# plt.show()

beacon_bounds = Polygon([(0, 0), (x_max, 0), (x_max, y_max), (0, y_max)])
print(beacon_bounds.area)


beacon_area = beacon_bounds.difference(combined_poly)

# plot_polygon(beacon_area)
# plt.gca().invert_yaxis()
# plt.show()
# print(type(beacon_area))

if type(beacon_area) == MultiPolygon:
    for poly in beacon_area.geoms:
        print(poly.centroid.x, poly.centroid.y)
else:
    print(beacon_area.centroid.x * 4_000_000 + beacon_area.centroid.y)

print('time taken: ', time.perf_counter() - start_time)
