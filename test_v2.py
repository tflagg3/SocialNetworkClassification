import numpy as np
import matplotlib.pyplot as plt
import ProcessWikivote
import ProcessEpinion
import random
from data_structures.subnetwork import Subnetwork
import test_v1

def run():
    ep_adj = ProcessEpinion.process_epinion()
    wk_adj = ProcessWikivote.process_wikivote()

    ep_subnets = []
    wk_subnets = []

    for i in range(0, 50):
        ep_subnet = generate_subnetwork(ep_adj)
        wk_subnet = generate_subnetwork(wk_adj)
        print('generated subnetworks ', i)
        ep_subnets.append(ep_subnet)
        wk_subnets.append(wk_subnet)

    # split our list of subnetworks into a
    ep_train = ep_subnets[:30]
    ep_test = ep_subnets[30:]

    wk_train = wk_subnets[:30]
    wk_test = wk_subnets[30:]


    # give us the sample statistics from the training data
    ai_ep_train = [i.generate_ai() for i in ep_train]
    ai_ep_train = tuple(zip(*ai_ep_train))
    ai_ep_train = [np.mean(i) for i in ai_ep_train]

    ai_wk_train = [i.generate_ai() for i in wk_train]
    ai_wk_train = tuple(zip(*ai_wk_train))
    ai_wk_train = [np.mean(i) for i in ai_wk_train]

    # convert to numpy??
    ai_ep_train = np.array(ai_ep_train)
    ai_wk_train = np.array(ai_wk_train)


    # test our epinion test data on the given ai averages
    ep_test_out = []
    wk_test_out = []
    for ep in ep_test:
        # put (NDep, NDwk) into test_out
        ai = np.array(ep.generate_ai())

        ep_distance = test_v1.normalized_distance(ai, ai_ep_train)
        wk_distance = test_v1.normalized_distance(ai, ai_wk_train)

        ep_test_out.append((ep_distance, wk_distance))

    # test our wikivote test data on the given ai averages
    for wk in wk_test:
        # put (NDep, NDwk) into test_out
        ai = np.array(wk.generate_ai())

        ep_distance = test_v1.normalized_distance(ai, ai_ep_train)
        wk_distance = test_v1.normalized_distance(ai, ai_wk_train)

        wk_test_out.append((ep_distance, wk_distance))

    # plot our results
    ep_x, ep_y = zip(*ep_test_out)
    wk_x, wk_y = zip(*wk_test_out)
    plt.scatter(ep_x, ep_y, color="blue", label="epinion data")
    plt.scatter(wk_x, wk_y, color="red", label="wikivote data")

    plt.title('predictions')
    plt.xlabel('normalized distance from epinion')
    plt.ylabel('normalized distance from wikivote')
    plt.legend()

    plt.savefig('test_v2_4.png')

    return ai_ep_train, ai_wk_train
def generate_subnetwork(adj):
    center_node = random.Random().randint(0, len(adj) - 1)
    num_nodes = random.Random().randint(150, 200)
    subnet = Subnetwork(center_node, num_nodes)
    # print('filling network...')
    subnet.fill_network_from_potential_neighbors(adj, center_node, [])
    subnet.fill_own_adj(adj)
    return subnet
