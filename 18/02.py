import re
from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import ast

with open('./18/input.txt') as f:
    lines = [tuple(int(i) for i in line.split(',')) for line in f.readlines()]


droplets = set()
agg = 0

maxx = max(x for x, y, z in lines)
maxy = max(y for x, y, z in lines)
maxz = max(z for x, y, z in lines)
print(maxx, maxy, maxz)

G: nx.Graph = nx.grid_graph(dim=(maxz + 2, maxy + 2, maxx + 2))

for node in G.nodes():
    G.nodes[node]['droplet'] = False

print('maxx:', max(x for x, y, z in G.nodes()))
print('maxy:', max(y for x, y, z in G.nodes()))
print('maxz:', max(z for x, y, z in G.nodes()))

print(G.edges((2, 2, 4)))

for x, y, z in lines:
    G.nodes[(x, y, z)]['droplet'] = True
    for dx, dy, dz in ((1, 0, 0), (0, 1, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 0, -1)):
        pot_neighbor = (x + dx, y + dy, z + dz)
        if G.nodes[pot_neighbor]['droplet'] == True:
            G.remove_edge((x, y, z), pot_neighbor)


for node in G.nodes():
    if G.nodes[node]['droplet'] == True:
        agg += G.degree(node)
print(agg)


G_nodroplet = G.copy()
G_nodroplet.remove_nodes_from([node for node in G_nodroplet.nodes() if G_nodroplet.nodes[node]['droplet'] == True])

for node in G_nodroplet.nodes():
    if G_nodroplet.nodes[node]['droplet'] == True:
        continue

    if not nx.has_path(G_nodroplet, node, (0, 0, 0)):
        print('removing node', node)
        G.remove_node(node)

agg = 0
for node in G.nodes():
    if G.nodes[node]['droplet'] == True:
        agg += G.degree(node)
print(agg)
