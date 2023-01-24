
import pickle

DEFAULT_WEIGHT = 1


class GraphException(Exception):
    pass


class Node:
    def __init__(self, name, edges=None, attrs=None):
        """
        @arg: name: string
        """
        self.name  = name

        # dict, key: next node name, val: weight int
        self.edges = edges if edges is not None else {}

        # dict, key: attribute name, val: property str
        self.attrs = attrs if attrs is not None else {}


class KnowledgeGraph:

    def __init__(self):
        self.nodes = {}  # key: node name (case sensitive), val: Node instance
        self.num_edges = 0


    def addNode(self, node_name, **args):
        """ idempotent operation """
        if node_name not in self.nodes:
            self.nodes[node_name] = Node(node_name)
        self.nodes[node_name].attrs.update(args)


    def updateNodeAttrs(self, node_name, **args):
        self.nodes[node_name].attrs.update(args)


    def addEdge(self, n1, n2, weight=DEFAULT_WEIGHT):
        """ idempotent operation """
        if n1 not in self.nodes or n2 not in self.nodes:
            msg = "Adding edge between nodes that do Not exist: "
            msg += "{} and {}".format(n1, n2)
            raise GraphException(msg)

        if not self.edgeExists(n1, n2):
            self.num_edges += 1

        self.nodes[n1].edges[n2] = weight
        self.nodes[n2].edges[n1] = weight


    def edgeExists(self, n1, n2):
        if n1 not in self.nodes or n2 not in self.nodes:
            return False
        return n2 in self.nodes[n1].edges


    def show(self):
        print("Num nodes = {}".format(len(self.nodes)))
        print("Num edges = {}".format(self.num_edges))
        for n in self.nodes:
            print("{} -- {}".format(n, [(k,v)
                  for k,v in self.nodes[n].attrs.items()]))
            for ee, ww in self.nodes[n].edges.items():
                print("    {}, {}".format(ee, ww))


    def save_graph(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self, fh)


    @staticmethod
    def load_graph(file_name):
        with open(file_name, 'rb') as fh:
            graph_obj = pickle.load(fh)
        return graph_obj

