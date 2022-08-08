
import networkx as nx
import matplotlib.pyplot as plt


class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def addNode(self, text):
        """ idempotent operation """
        text = text.strip().lower()
        if text:
            self.graph.add_node(text)

    def addEdge(self, n1, n2, **args):
        self.graph.add_edge(n1, n2, **args)

    def show(self):
        s_layout = nx.spring_layout(self.graph)
        nx.draw(self.graph, s_layout, with_labels=True)
        node_labels = nx.get_node_attributes(self.graph, 'label')
        nx.draw_networkx_labels(self.graph, s_layout, labels = node_labels)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, s_layout, edge_labels)
        plt.show()

