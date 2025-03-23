import ProcessWikivote, ProcessSlashdot, ProcessFB, ProcessEpinion, ProcessGNutella5, ProcessGNutella6, ProcessGNutella24, ProcessGNutella30
import random
from data_structures.subnetwork import Subnetwork
import numpy as np
import pdb
import pickle


def run():

    print("Starting!")
    # first we process in our datasets into adjacency matrices
    data_processors = [ProcessFB, ProcessWikivote, ProcessSlashdot, ProcessEpinion, ProcessGNutella5, ProcessGNutella6, ProcessGNutella24, ProcessGNutella30]
    adjs = [processor.process() for processor in data_processors]
    print("processed data!")
    print("generating subnetworks...")

    # then we will want to generate the subnetworks
    all_subnets = [[] for i in range(len(adjs))]
    for i, adj in enumerate(adjs):
        print("finished subnets generation ", i)
        for j in range(0, 50):
            all_subnets[i].append(generate_subnetwork(adj))

    # split into a train and a test set for each network
    train_subnets = [subnets[:30] for subnets in all_subnets]
    test_subnets = [subnets[30:] for subnets in all_subnets]
    print("split the subnetworks into train and test subnetworks!")
    print("generating ai for training subnetworks...")

    # generate ai and average it for each training set
    mean_ais = []
    for x, subnets in enumerate(train_subnets):
        print("finished ai generation ", x)
        ais = [subnet.generate_ai() for subnet in subnets]
        zipped = zip(*ais)
        mean_ai = [np.mean(i) for i in zipped]
        mean_ais.append(mean_ai)

    print("finished generating ai for training subnetworks!")
    # generate ai for test subnets, guess which one
    all_guesses = []
    for subnets in test_subnets:
        ais = [subnet.generate_ai() for subnet in subnets]
        guesses = []
        for ai in ais:
            # generate the distance to each train data
            distances = [normalized_distance(ai, mean_ai) for mean_ai in mean_ais]
            dist_min = min(distances)
            if distances.count(dist_min) > 1:
                print(distances.count(dist_min), ' matches found')
            guesses.append(distances.index(dist_min))
        all_guesses.append(guesses)


    # pickle our output data data...
    with open("test_v3_guesses_1.pickle", "wb") as file:
        pickle.dump(all_guesses, file)

    print(all_guesses)

def generate_subnetwork(adj):
    center_node = random.Random().randint(0, len(adj) - 1)
    num_nodes = random.Random().randint(150, 200)
    subnet = Subnetwork(center_node, num_nodes)
    subnet.fill_network_from_potential_neighbors(adj, center_node, [])
    subnet.fill_own_adj(adj)
    return subnet

def normalized_distance(a, b):
    output = 0
    # pdb.set_trace()
    for x, comp in enumerate(a):
        temp = abs(comp - b[x])
        output += temp/b[x]

    if output > 10:
        pdb.set_trace()

    return output