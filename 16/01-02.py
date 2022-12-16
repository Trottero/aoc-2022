import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

with open('./16/input.txt') as f:
    lines = [line.split(' ') for line in f.readlines()]

G = nx.Graph()

for line in lines:
    node_id = line[1]
    flow_rate = int(line[4][5:-1])

    G.add_node(node_id)
    G.nodes[node_id]['flow_rate'] = flow_rate

    connects_to = [l.replace(',', ' ').strip() for l in line[9:]]
    for connect in connects_to:
        G.add_edge(node_id, connect, weight=1)


def dfs(graph: nx.Graph, current_node: int, path: list, open_nodes: list, score: int, minutes_left: int):
    # Surely we can do a dfs with a max depth of 30 right????
    if minutes_left <= 0:
        return score

    # Explore all options where we do not open the neighboring node
    max_score = 0
    for n in graph.neighbors(current_node):
        # Update score
        score += sum(graph.nodes[n]['flow_rate'] for n in open_nodes)
        max_score = dfs(graph, n, path + [n], open_nodes, score, minutes_left - 1)

    # Explore all options where we do open the neighboring node
    for n in graph.neighbors(current_node):
        score += graph.nodes[n]['flow_rate']
        if n not in open_nodes:
            max_score = max(max_score, dfs(graph, n, path + [n], open_nodes + [n], score, minutes_left - 2))
        else:
            # Node already open
            max_score = max(max_score, dfs(graph, n, path + [n], open_nodes, score, minutes_left - 1))

    return max_score


flow_rates = []
current_node = 'AA'
minutes_left = 30

print(dfs(G, current_node, [current_node], [], 0, minutes_left))
