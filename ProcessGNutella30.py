import numpy as np


def process():
    with open('data/p2p-Gnutella24.txt', 'r') as nutella:
        text = nutella.read()

    adj = np.identity(36682)
    lines = text.split('\n')
    for line in lines:
        if line[0] == '#':
            continue

        (node_from, node_to) = line.split('\t')
        adj[int(node_from), int(node_to)] = 1

    return adj