
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


    def get_next_nodes(self, cur_lemmas):
        """
        arg: cur_lemmas = list of strings
        arg: visited = list of node names already visited
        return: tuple (cur_lemmas, <dict-of-next-nodes>)
            cur_lemmas = same list of words, but their lemmas
            dict: key = next node name, val = num times node hit
        """
        # key = node name, value = strength of relationship
        nodes_dict = defaultdict(lambda: 0)
        tokens = nlp(' '.join(cur_lemmas))
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


    def iterate_graph(self, start_words, max_hops=5):
        """
        arg: start_words = list of strings to start searching graph with
        arg: max_hops = max breadth-first-search depth
        return: dict of visited nodes
            key = lemma of word
            val = num times word was hit when traversing the graph
        """
        tokens = nlp(' '.join(start_words))
        start_lemmas = [tok.lemma_ for tok in tokens]

        visited_dict = defaultdict(lambda: 0)
        cur_lemmas, next_dict = self.get_next_nodes(start_lemmas)
        counter = 0

        while next_dict:
            counter += 1
            if counter > max_hops:
                break

            for cur_lemma in cur_lemmas:
                visited_dict[cur_lemma] += 1

            next_keys = [x for x in next_dict.keys()]
            for key in next_keys:
                if key in visited_dict:
                    visited_dict[key] += next_dict[key]
                    del next_dict[key]

            cur_lemmas, next_dict = self.get_next_nodes(next_dict.keys())

        return visited_dict


