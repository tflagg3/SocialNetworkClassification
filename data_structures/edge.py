
class Edge(object):
    def __init__(self, node1, node_2):
        self.node1 = node1
        self.node2 = node_2

    def __eq__(self, other):
        return ((self.node1 == other.node1 and self.node2 == other.node2)
                or (self.node1 == other.node2 and self.node2 == other.node1))