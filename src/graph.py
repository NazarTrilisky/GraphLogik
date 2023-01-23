
import pickle
from collections import defaultdict


class GraphException(Exception):
    pass


class Node:
    def __init__(self, name, edges=defaultdict(lambda: {}), attrs={}):
        """
        @arg: name: string
        """
        self.name  = name
        self.edges = edges  # dict with key = next node name, val = weight int
        self.attrs = attrs  # dict with key = attribute name, attribute value string


class KnowledgeGraph:

    def __init__(self):
        # key = node name (case sensitive)
        # val = Node class instance
        self.graph = {}
        self.num_edges = 0


    def addNode(self, node_name, **args):
        """ idempotent operation """
        if node_name in self.graph:
            self.graph[node_name].attrs.update(args)
        else:
            self.graph[node_name] = Node(node_name)


    def addEdge(self, n1, n2, weight=1):
        """ idempotent operation """
        if n1 not in self.graph or n2 not in self.graph:
            msg = "Adding edge between nodes that do Not exist: "
            msg += "{} and {}".format(n1, n2)
            raise GraphException(msg)

        if not self.edgeExists(n1, n2):
            self.num_edges += 1

        self.graph[n1].edges[n2] = weight
        self.graph[n2].edges[n1] = weight


    def edgeExists(self, n1, n2):
        if n1 not in self.graph or n2 not in self.graph:
            return False
        return n2 in self.graph[n1].edges


    def show(self):
        print("Num nodes = {}".format(len(self.graph)))


    def save_graph(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self, fh)


    @staticmethod
    def load_graph(file_name):
        with open(file_name, 'rb') as fh:
            graph_obj = pickle.load(fh)
        return graph_obj

