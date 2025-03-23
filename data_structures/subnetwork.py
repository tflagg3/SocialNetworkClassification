import pdb
import random
import numpy as np
from scipy.stats import kurtosis, skew, describe

class Subnetwork(object):
    def __init__(self, center_node, size):
        self.center_node = center_node
        self.size = size
        self.nodes = [center_node]
        self.adj_mat = np.zeros([size, size])


    def fill_network_from_potential_neighbors(self, adjacency_list, node, potential_neighbors=[]):

        # pdb.set_trace()
        if len(self.nodes) == self.size:
            return

        to_idxs = adjacency_list[node, :].nonzero()[0]
        from_idxs = adjacency_list[:, node].nonzero()[0]
        neighbors = to_idxs.tolist() + from_idxs.tolist()
        new_neighbors = [neighbor for neighbor in neighbors if neighbor not in self.nodes]
        potential_neighbors.extend(new_neighbors)
        neighbor = random.choice(potential_neighbors)
        self.nodes.append(neighbor)
        potential_neighbors.remove(neighbor)
        self.fill_network_from_potential_neighbors(adjacency_list, neighbor, potential_neighbors)
        return



    def fill_network_one_at_a_time(self, adjacency_list, node):


        # pdb.set_trace()
        if len(self.nodes) == self.size:
            return

        # remove duplicates?
        to_idxs = adjacency_list[node, :].nonzero()[0]
        from_idxs = adjacency_list[:, node].nonzero()[0]
        neighbors = to_idxs.tolist() + from_idxs.tolist()
        neighbor = random.choice(neighbors)

        if neighbor not in self.nodes:
            self.nodes.append(neighbor)

        self.fill_netowrk_one_at_a_time(adjacency_list, random.choice(self.nodes))


    def fill_network_all_center_neighbors(self, adjacency_list, current_node=None):

        if current_node is None:
            current_node = self.center_node
        to_edges = adjacency_list[current_node, :]
        from_edges = adjacency_list[:, current_node]
        to_idxs = to_edges.nonzero()[0]
        from_idxs =  from_edges.nonzero()[0]

        for idx in to_idxs:
            if idx in self.nodes:
                continue
            self.nodes.append(idx)
            if len(self.nodes) == self.size:
                # full node list
                return

        for idx in from_idxs:
            if idx in self.nodes:
                continue
            self.nodes.append(idx)
            if len(self.nodes) == self.size:
                # full node list
                return

        self.fill_network_all_center_neighbors(adjacency_list,
                                               current_node=self.nodes[random.Random().randint(0,len(self.nodes)-1)])

        return

    def fill_own_adj(self, full_adj):
        # pdb.set_trace()
        for node_idx, node in enumerate(self.nodes):
            to_edges = full_adj[node, :]
            to_nodes = to_edges.nonzero()[0]
            from_nodes = full_adj[:, node].nonzero()[0]
            nodes = to_nodes.tolist() + from_nodes.tolist()
            for i in nodes:
                if i not in self.nodes:
                    continue
                if i == node:
                    continue
                i_idx = self.nodes.index(i)
                self.adj_mat[node_idx, i_idx] = 1
                self.adj_mat[i_idx, node_idx] = 1
        return

    def generate_ai(self):

        degree_centralities = []
        closeness_centralities = []
        for x, node in enumerate(self.nodes):

            # calculate degree of centrality and append
            unique, counts = np.unique(self.adj_mat[:, x], return_counts=True)
            # try:
            connections = counts[1]
            # except IndexError:
            #     connections = 0
            degree_centralities.append(connections / (self.size - 1))

            # calculate closeness centrality
            ejk = 0
            node_adj = self.adj_mat[x, :]
            node_neighbors = node_adj.nonzero()[0]
            for neighbor in node_neighbors:
                neighbor_adj = self.adj_mat[neighbor, :]
                neighbor_neighbors = neighbor_adj.nonzero()[0]
                for neighbor_neighbor in neighbor_neighbors:
                    if neighbor_neighbor in node_neighbors:
                        # existence of triad found
                        # triggers twice for each triad because of matrix structure
                        ejk += 1
            # is this how degree 1 ends up with lots of division by zero so this avoids that
            # not sure whether it is the correct solution or not

            if counts[1] != 1:
                cc = (ejk / (counts[1] * (counts[1] - 1)))
            else:
                cc = ejk
            closeness_centralities.append(cc)

        # want to get mean, var, skewness, kurtosis of each of the
        cc_result = describe(closeness_centralities)
        dc_result = describe(degree_centralities)

        output = (dc_result.mean,
                  dc_result.variance,
                  dc_result.skewness,
                  dc_result.kurtosis,
                  cc_result.mean,
                  cc_result.variance,
                  cc_result.skewness,
                  cc_result.kurtosis,
        )




        return output
