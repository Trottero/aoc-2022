import numpy as np
import networkx as nx

with open ('./07/input.txt') as f:
    lines = [line.strip() for line in f.readlines()]

def node_name(path):
    return "".join(path)

G = nx.DiGraph()

G.add_node('/')

path = ['/']
it = 0
for it, line in enumerate(lines):
    if line.startswith('$ cd'):
        arg = line.split(' ')[-1].strip()
        if arg == '/':
            path = ['/']
            continue
        if arg == '..':
            path = path[:-1]
            continue
    
        path.append(f'{arg}/')
        G.add_edge(node_name(path[:-1]), node_name(path))
        continue

    if line.startswith('$ ls'):
        # Expand dir
        folder_size = 0
        for inner_line in lines[it+1:]:
            if inner_line.startswith('$'):
                break
            if not inner_line.startswith('dir '):
                folder_size += int(inner_line.split(' ')[0])

        G.nodes[node_name(path)]['folder_size'] = folder_size

print(G.nodes)

def expand_node(G: nx.DiGraph, node):
    if G.out_degree(node) != 0:
        for child in G.neighbors(node):
            G.nodes[node]['folder_size'] += expand_node(G, child)

    return G.nodes[node]['folder_size']

expand_node(G, '/')

print(sum([G.nodes[node]['folder_size'] for node in G.nodes if G.nodes[node]['folder_size'] <= 100000]))