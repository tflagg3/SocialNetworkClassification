from data_structures.subnetwork import Subnetwork
import numpy as np

def process():
    with open ('data/wiki-Vote.txt', 'r') as wikivote:
        text = wikivote.read()

    adj = np.identity(7115)
    lines = text.split('\n')
    nodes = []
    for line in lines:
        if line[0] == '#':
            continue
        (node_from, node_to) = line.split('\t')
        if node_from not in nodes:
            nodes.append(node_from)
        if node_to not in nodes:
            nodes.append(node_to)

        adj[nodes.index(node_from), nodes.index(node_to)] = 1


    return adj