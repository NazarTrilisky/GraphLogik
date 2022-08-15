
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

    def get_next_nodes(self, cur_nodes):
        """
        arg: cur_nodes = list of strings
        arg: visited = list of node names already visited
        return: tuple (cur_lemmas, <dict-of-next-nodes>)
            cur_lemmas = same list of words, but their lemmas
            dict: key = next node name, val = num times node hit
        """
        # key = node name, value = strength of relationship
        nodes_dict = defaultdict(lambda: 0)
        tokens = nlp(' '.join(cur_nodes))
        cur_lemmas = []
        for token in tokens:
            cur_lemmas.append(token.lemma_)
            try:
                cur_nbrs = self.graph.neighbors(token.lemma_)
            except NetworkXError as err:
                if 'not in the graph' in str(err).lower():
                    continue
                else:
                    raise err

            neighbors = [n for n in cur_nbrs]
            for nbr in neighbors:
                nodes_dict[nbr] += 1

        return cur_lemmas, nodes_dict



