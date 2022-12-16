import re
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

with open('./16/input.txt') as f:
    lines = [line.split(' ') for line in f.readlines()]

G = nx.DiGraph()

for line in lines:
    node_id_flow = line[1]+'_flow'
    node_id_skip = line[1]+'_skip'
    flow_rate = int(line[4][5:-1])

    G.add_node(node_id_flow)
    G.add_node(node_id_skip)
    G.nodes[node_id_flow]['flow_rate'] = flow_rate
    G.nodes[node_id_flow]['visisted'] = False

    G.nodes[node_id_skip]['flow_rate'] = 0
    G.nodes[node_id_skip]['visisted'] = False

    connects_to = [l.replace(',', ' ').strip() for l in line[9:]]
    for connect in connects_to:
        connect_flow = connect+'_flow'
        connect_skip = connect+'_skip'
        G.add_edge(node_id_skip, connect_flow, weight=2)
        G.add_edge(node_id_skip, connect_skip, weight=1)
        G.add_edge(node_id_flow, connect_flow, weight=2)
        G.add_edge(node_id_flow, connect_skip, weight=1)


def greedy_next(Graph: nx.Graph, current: str, minutes_left: int):
    # Get all neighbors of the current node
    neighbors = list(n for n in Graph.neighbors(current) if not Graph.nodes[n]['open'])
    # Select neighbor with the highest flow rate
    return max(neighbors, key=lambda x: Graph.nodes[x]['flow_rate'])


def greedy_open(Graph: nx.Graph, current: str, minutes_left: int):
    if Graph.nodes[current]['open'] == False:
        return Graph.nodes[current]['flow_rate'] > 0
    return False


def smart_next(Graph: nx.Graph, current: str, minutes_left: int):
    # Get distance from this node to all other nodes
    distances = nx.shortest_path(Graph, current, weight='weight')

    pressure_potential = {k: (minutes_left - len(v) - 2) * Graph.nodes[k]['flow_rate']
                          for k, v in distances.items() if not Graph.nodes[k]['open']}

    target_node = max(pressure_potential, key=lambda x: pressure_potential[x])
    # Select node with the highest pressure potential
    return target_node, len(distances[target_node]) - 1


# print all nodes their openness state
for node in G.nodes:
    print(node, G.nodes[node]['open'])

flow_rates = []
current_node = 'AA'
minutes_left = 30

path = []
# Greedely traverse the graph in an attempt to find a path which maximizes the time that the flow rate has been active
# It takes 1 minute to traverse from node to node, and one minute there to open it.
while minutes_left > 0:
    # Compute the sum of all flow rates which have open valves
    flow_rates.append(sum(G.nodes[n]['flow_rate'] for n in G.nodes if G.nodes[n]['visited']))

    # Check if the current node is open
    if G.nodes[current_node]['open'] == False:
        # Check if it is even worth opening
        if greedy_open(G, current_node, 0):
            # If the value is greater than 0, open the node
            G.nodes[current_node]['open'] = True
            # This action takes 1 minute
            minutes_left -= 1
            continue

    # Find the next node
    current_node, time_taken = smart_next(G, current_node, minutes_left)
    if time_taken == 0:
        time_taken = 1
    path.append(current_node)
    if time_taken > 1:
        flow_rates_sum = sum(G.nodes[n]['flow_rate'] for n in G.nodes if G.nodes[n]['open'])
        for i in range(time_taken - 1):
            flow_rates.append(flow_rates_sum)

    minutes_left -= time_taken

print(path)
print(flow_rates)
print(sum(flow_rates))
print(len(flow_rates))
