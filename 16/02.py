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


class Actor:
    def __init__(self, node_id: int):
        self.position: int = node_id
        self.stall: int = 0
        self.target: int = None

    def copy(self):
        a = Actor(self.position)
        a.stall = self.stall
        a.target = self.target
        return a

    def has_target(self):
        return self.target is not None


def get_path_cost(graph: nx.Graph, source, target):
    path = nx.dijkstra_path(graph, source, target, weight='weight')
    path_cost = 0
    cn = path[0]
    for next_in_path in path[1:]:
        path_cost += graph.edges[cn, next_in_path]['weight']
        cn = next_in_path

    return path_cost


def dfs(graph: nx.Graph, elephant: Actor, human: Actor, open_nodes: list, score: int, minutes_left: int):

    if len(open_nodes) == len(graph.nodes):
        # All nodes are open, no need to wait
        return score + (minutes_left * sum(graph.nodes[n]['flow_rate'] for n in graph.nodes()))

    elephant_copy = elephant.copy()
    human_copy = human.copy()
    open_nodes_copy = open_nodes.copy()

    min_stall = min([elephant_copy.stall, human_copy.stall, minutes_left])

    new_score = score + (min_stall * sum(graph.nodes[n]['flow_rate'] for n in open_nodes_copy))

    minutes_left -= min_stall
    elephant_copy.stall -= min_stall
    human_copy.stall -= min_stall

    if minutes_left <= 0:
        return new_score

    # Check if any of the actors have reached their destination
    for actor in [human_copy, elephant_copy]:
        if actor.stall > 0:
            continue
        # If it had a target, add it to the open nodes and reset the target
        if actor.has_target():
            open_nodes_copy.append(actor.target)
            actor.position = actor.target
            actor.target = None

    scores = []
    for node_ind, potential_target in enumerate(graph.nodes()):
        if potential_target in open_nodes_copy or potential_target in [
                human_copy.position, elephant_copy.position, human_copy.target, elephant_copy.target]:
            # Assume that we just wait here
            scores.append(new_score + (minutes_left * sum(graph.nodes[d]['flow_rate'] for d in open_nodes_copy)))
            continue

        # Attempt to assign a target to the actors
        for actor in [human_copy, elephant_copy]:
            # Check if actor already has a target
            if actor.has_target():
                continue

            # check if the potential target is already taken by another agent
            if potential_target in [human_copy.target, elephant_copy.target]:
                continue

            # We found a valid potential target, find a path to it.
            actor.target = potential_target
            path_cost = get_path_cost(graph, actor.position, potential_target)
            # +1 because we need to wait one minute at the target node to activate it
            actor.stall = path_cost + 1

        # Both check if both actors have a target, or if we are at the last node
        if human_copy.has_target() and elephant_copy.has_target():
            # if human_copy.has_target() and elephant_copy.has_target():
            path_score = dfs(graph, elephant_copy, human_copy, open_nodes_copy, new_score, minutes_left)
            scores.append(path_score)

    return max(scores)


flow_rates = []
current_node = 'AA'
minutes_left = 26

summm = sum(G.nodes[n]['flow_rate'] for n in G.nodes)

human = Actor('AA')
elephant = Actor('AA')

print(dfs(G, human, elephant, [], 0, minutes_left))
