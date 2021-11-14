
import networkx as nx
import matplotlib.pyplot as plt


class KnowledgeGraph:
    def __init__(self):
        self.graph = nx.Graph()

    def addNode(self, text):
        """ idempotent operation """
        text = text.strip().lower()
        self.graph.add_node(text.strip().lower())

    def connect(self, n1, n2, weight=1):
        self.graph.add_weighted_edges_from([(n1, n2, weight)])

    def show(self):
        s_layout = nx.spring_layout(self.graph)
        nx.draw(self.graph, s_layout, with_labels=True)
        node_labels = nx.get_node_attributes(self.graph, 'weight')
        nx.draw_networkx_labels(self.graph, s_layout, labels = node_labels)
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, s_layout, edge_labels)
        plt.show()


if __name__ == '__main__':
    kg = KnowledgeGraph()
    kg.addNode("brush")
    kg.addNode("teeth")
    kg.addNode("floss")
    kg.addNode("cavities")
    kg.connect("brush", "teeth", .9)
    kg.connect("floss", "teeth", .8)
    kg.connect("brush", "cavities", -1)
    kg.connect("floss", "brush", .95)
    kg.connect("cavities", "floss", -.9)
    kg.show()

