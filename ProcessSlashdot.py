import numpy as np

def process():

    with open('data/soc-Slashdot0811.txt', 'r') as slash:
        text = slash.read()

    adj = np.identity(77360)
    lines = text.split('\n')
    for line in lines:
        if line[0] == '#':
            continue

        (node_from, node_to) = line.split('\t')
        adj[int(node_from), int(node_to)] = 1

    return adj

