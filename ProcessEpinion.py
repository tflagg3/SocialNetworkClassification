import random
import data_structures.subnetwork as subnetwork
import numpy as np

# takes a path to the txt file
def process():
    with open ('data/epinion.txt', 'r') as epinion:
        text = epinion.read()


    # prepare our adjacency matrix
    adjacency_matrix = np.identity(75888)
    lines = text.split('\n')
    out_nodes = []
    for line in lines:
        # ignore comment lines
        if line[0] == '#':
            continue

        (node_from, node_to) = line.split('\t')
        adjacency_matrix[int(node_from), int(node_to)] = 1

    return adjacency_matrix


def generate_subnetwork(adjacency_matrix):
    center_node = random.Random().randint(0, len(adjacency_matrix) - 1)
    num_nodes = random.Random().randint(150, 200)
    subnet = subnetwork.Subnetwork(center_node, num_nodes)
    subnet.fill_network_all_center_neighbors(adjacency_matrix)
    subnet.fill_own_adj(adjacency_matrix)
    return subnet

def test_adj_mat(adjacency_matrix):
    zero_cnt = 0
    one_cnt = 0
    two_cnt = 0
    for n in range(75888):
        for k in range(75888-n):
            cnt = 0
            cnt += adjacency_matrix[n][n+k] + adjacency_matrix[n+k][n]
            if cnt == 0:
                zero_cnt += 1
            elif cnt == 1:
                one_cnt += 1
            elif cnt == 2:
                two_cnt += 1



    print('Adjacency matrix data')
    print('--------------------------------------')
    print('No edges: ', zero_cnt)
    print('Edges in one direction: ', one_cnt)
    print('Edges in two directions: ', two_cnt)