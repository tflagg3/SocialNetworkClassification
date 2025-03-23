import csv
import numpy as np



def process():
    # # generate a blank adjacency matrix
    adj = np.identity(37700)
    # open the relevant file
    with open('data/git_web_ml/musae_git_edges.csv', 'r') as fb:
        data = csv.DictReader(fb)
        for n, edge in enumerate(data):
            # parse the ids to ints
            id_1 = int(edge['id_1'])
            id_2 = int(edge['id_2'])
            adj[id_1, id_2] = 1
            adj[id_2, id_1] = 1

    return adj

def generate_subnetwork():
    # pick a subnetwork
    #

    pass