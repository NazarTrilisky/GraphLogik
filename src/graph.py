
import spacy
import networkx as nx
from networkx.exception import NetworkXError
import matplotlib.pyplot as plt

from collections import defaultdict


nlp = spacy.load('en_core_web_sm')


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

    def get_next_nodes(self, keywords):
        """
        arg: keywords = list of strings
        return: dict: key = next node name, val = num times node hit
        """
        # key = node name, value = strength of relationship
        nodes_dict = defaultdict(lambda: 0)
        tokens = nlp(' '.join(keywords))
        for token in tokens:
            try:
                cur_nbrs = self.graph.neighbors(token.lemma_)
            except NetworkXError as err:
                if 'not in the graph' in str(err).lower():
                    continue
                else:
                    raise err

            neighbors = [n for n in cur_nbrs]
            for n in neighbors:
                nodes_dict[n] += 1

        return nodes_dict


