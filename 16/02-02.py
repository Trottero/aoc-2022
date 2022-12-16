import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


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


def has_0_flowrate_nodes(graph: nx.Graph):
    for node in graph.nodes:
        if is_0_flowrate_node(graph, node):
            return True
    return False


def is_0_flowrate_node(graph: nx.Graph, node: int):
    return graph.nodes[node]['flow_rate'] == 0 and node != 'AA'


print(G)


def compress_graph(graph: nx.Graph):
    # Find all nodes that have a flowrate of 0 so we can compress.
    while has_0_flowrate_nodes(graph):
        for node in graph.nodes:
            if graph.nodes[node]['flow_rate'] == 0 and node != 'AA':
                # Compress this node
                neighbors = list(graph.neighbors(node))
                # Get all pairs
                for n1, n2 in combinations(neighbors, 2):
                    # Check if n1 and n2 are connected
                    if graph.has_edge(n1, n2):
                        continue

                    # Add edge between the two nodes with the combined weight
                    w1 = graph.edges[n1, node]['weight']
                    w2 = graph.edges[n2, node]['weight']
                    graph.add_edge(n1, n2, weight=w1 + w2)

                graph.remove_node(node)
                break

    return graph


G = compress_graph(G)
print(G)

# pos = nx.spring_layout(G, seed=7)
# nx.draw(G, with_labels=True, pos=pos)
# edge_labels = nx.get_edge_attributes(G, "weight")
# nx.draw_networkx_edge_labels(G, pos, edge_labels)
# plt.show()


def dfs(graph: nx.Graph, current_node: int, open_nodes: list, score: int, minutes_left: int):
    # Surely we can do a dfs with a max depth of 30 right????
    if minutes_left <= 0:
        return score, open_nodes

    if len(open_nodes) == len(graph.nodes):
        # All nodes are open, no need to wait
        return score + (minutes_left * sum(graph.nodes[n]['flow_rate'] for n in graph.nodes())), open_nodes

    scores = []
    # Select a destination node which is not open
    for n in graph.nodes():
        # Check if already opened or the current node
        if n in open_nodes or n == current_node:
            # If it is, there's no reason to go there and thus we can skip it.
            new_score = score + (minutes_left * sum(graph.nodes[d]['flow_rate'] for d in open_nodes))
            scores.append((new_score, open_nodes.copy()))
            continue

        shortest_path = nx.dijkstra_path(graph, current_node, n, weight='weight')
        path_cost = 0
        cn = current_node
        for node in shortest_path[1:]:
            path_cost += graph.edges[cn, node]['weight']
            cn = node

        # Check if the path cost doesnt exceed the minutes left
        if path_cost >= minutes_left:
            # Compute the score that would be added when traversing towards the target node
            new_score = score + (minutes_left * sum(graph.nodes[d]['flow_rate'] for d in open_nodes))
            # This makes it an invalid path, and thus we get to wait here.
            scores.append((new_score, open_nodes.copy()))
            continue

        new_score = score + ((path_cost + 1) * sum(graph.nodes[d]['flow_rate'] for d in open_nodes))
        # If there's still space to explore, we can explore further
        t = dfs(graph, n, open_nodes + [n], new_score, minutes_left - path_cost - 1)
        scores.append(t)

    return max(scores, key=lambda x: x[0])


flow_rates = []
current_node = 'AA'
minutes_left = 26

score1, nodes1 = dfs(G, current_node, [], 0, minutes_left)
print('done with first dfs')
for node in nodes1:
    G.nodes[node]['flow_rate'] = 0

score2, nodes2 = dfs(G, current_node, [], 0, minutes_left)

print(score1, score2, 'sum:', score1 + score2)
