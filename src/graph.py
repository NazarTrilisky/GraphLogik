
import spacy
import networkx as nx
from networkx.exception import NetworkXError
import matplotlib.pyplot as plt

from collections import defaultdict


nlp = spacy.load('en_core_web_sm')


class KnowledgeGraph:

    def __init__(self):
        self.graph = nx.Graph()


    def addNode(self, text, **args):
        """ idempotent operation """
        self.graph.add_node(text.strip().lower(), **args)


    def addLabelToNode(self, node_name, label_str):
        if node_name.strip() and label_str.strip():
            if not node_name in self.graph.nodes:
                self.graph.add_node(node_name.strip().lower(), label=label_str)
            else:
                cur_node = self.graph.nodes[node_name]
                if 'label' not in cur_node.keys():
                    cur_node['label'] = label_str
                else:
                    cur_node['label'] += label_str


    def addEdge(self, n1, n2, **args):
        self.graph.add_edge(n1.strip().lower(), n2.strip().lower(), **args)


    def draw_graph(self):
        s_layout = nx.spring_layout(self.graph)
        node_labels_layout = \
            {n:(x, y+0.1) for n,(x,y) in s_layout.items()}

        nx.draw(self.graph, s_layout, with_labels=True)
        node_labels = nx.get_node_attributes(self.graph, 'label')
        nx.draw_networkx_labels(self.graph, node_labels_layout,
                                labels=node_labels)
        edge_labels = nx.get_edge_attributes(self.graph, 'label')
        nx.draw_networkx_edge_labels(self.graph, s_layout, edge_labels)


    def show(self):
        self.draw_graph()
        plt.show()


    def save(self, name="graph_image.png"):
        self.draw_graph()
        plt.savefig(name)

