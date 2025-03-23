import pdb
import ProcessEpinion
import ProcessWikivote
import numpy as np
import matplotlib.pyplot as plt

def run():
    ep_adj = ProcessEpinion.process_epinion()
    wk_adj = ProcessWikivote.process_wikivote()
    ep_subnets = []
    wk_subnets = []
    for i in range(0, 100):
        ep_subnet = ProcessEpinion.generate_subnetwork(ep_adj)
        # pdb.set_trace()
        wk_subnet = ProcessEpinion.generate_subnetwork(wk_adj)
        ep_subnets.append(ep_subnet)
        wk_subnets.append(wk_subnet)


    ep_train = ep_subnets[:60]
    ep_test = ep_subnets[60:]

    wk_train = wk_subnets[:60]
    wk_test = wk_subnets[60:]

    ai_ep_train = [i.generate_ai() for i in ep_train]
    ai_ep_train = tuple(zip(*ai_ep_train))
    ai_ep_train = [np.mean(i) for i in ai_ep_train]

    ai_wk_train = [i.generate_ai() for i in wk_train]
    ai_wk_train = tuple(zip(*ai_wk_train))
    ai_wk_train = [np.mean(i) for i in ai_wk_train]

    print('epinion data: \n ---------------------- \n', ai_ep_train)
    print("wikivote data: \n----------------------- \n",ai_wk_train)

    ai_ep_train = np.array(ai_ep_train)
    ai_wk_train = np.array(ai_wk_train)

    ep_test_out = []
    wk_test_out = []
    for ep in ep_test:
        # put (NDep, NDwk) into test_out
        ai = np.array(ep.generate_ai())

        ep_distance = normalized_distance(ai, ai_ep_train)
        wk_distance = normalized_distance(ai, ai_wk_train)

        ep_test_out.append((ep_distance, wk_distance))

    for wk in wk_test:
        # put (NDep, NDwk) into test_out
        ai = np.array(wk.generate_ai())

        ep_distance = normalized_distance(ai, ai_ep_train)
        wk_distance = normalized_distance(ai, ai_wk_train)

        wk_test_out.append((ep_distance, wk_distance))



    # plot
    ep_x, ep_y = zip(*ep_test_out)
    wk_x, wk_y = zip(*wk_test_out)
    plt.scatter(ep_x, ep_y, color="blue", label="epinion data")
    plt.scatter(wk_x, wk_y, color="red", label="wikivote data")

    plt.title('predictions')
    plt.xlabel('normalized distance from epinion')
    plt.ylabel('normalized distance from wikivote')
    plt.legend()

    plt.savefig('test_6.png')

    return ai_ep_train, ai_wk_train

def normalized_distance(a, b):
    output = 0
    # pdb.set_trace()
    for x, comp in enumerate(a):
        temp = abs(comp - b[x])
        output += temp/b[x]

    if output > 10:
        pdb.set_trace()

    return output