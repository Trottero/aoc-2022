from typing import List
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

with open('./12/input.txt') as f:
    lines = [[x for x in line.strip()] for line in f.readlines()]

x_size = len(lines[0])
y_size = len(lines)

G: nx.Graph = nx.grid_graph(dim=(y_size, x_size))

# node_locs = {node: (node[0], y_size - node[1]) for node in G.nodes()}
# nx.draw(G, with_labels=True, pos=node_locs)
# plt.show()

# print([v for u, v in G.edges(1)])

for y, line in enumerate(lines):
    for x, node_val in enumerate(line):
        node_id = (x, y)
        G.nodes[node_id]['label'] = node_val
        if node_val == 'S':
            start_node = node_id
            G.nodes[node_id]['val'] = 0
            continue
        if node_val == 'E':
            end_node = node_id
            G.nodes[node_id]['val'] = 25
            continue
        G.nodes[node_id]['val'] = int(node_val, 36) - 10

# Convert graph into directed graph
G = G.to_directed()

for edge in G.edges():
    # Update the edge weight to be the difference of the two nodes
    G.edges[edge]['computed_weight'] = int(G.nodes[edge[1]]['val'] - G.nodes[edge[0]]['val'])

# Part 1 specific: remove all of the edges which are larger than 1
to_remove = []
for edge in G.edges():
    if G.edges[edge]['computed_weight'] > 1:
        to_remove.append(edge)
G.remove_edges_from(to_remove)

# node_locs = {node: (node[0], y_size - node[1]) for node in G.nodes()}
# nx.draw(G, with_labels=True, pos=node_locs)
# plt.show()

# Compute the shortest path from start to end
paths = nx.single_target_shortest_path(G, end_node)

# filter out the paths that start with a node of a value of 0
paths = {k: v for k, v in paths.items() if G.nodes[k]['val'] == 0}

# find the shortest path
path = min(paths.values(), key=len)

print(path)
print(len(path) - 1)  # -1 for the starting node ;)
