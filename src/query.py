
import spacy
from networkx.exception import NetworkXError

from collections import defaultdict


nlp = spacy.load('en_core_web_sm')


def get_next_nodes(kg, node_names):
    """
    arg: kg = KnowledgeGraph object
    arg: node_names = list of strings
    arg: visited = list of node names already visited
    return: <dict-of-next-nodes>
        dict: key = next node name, val = num times node hit
    """
    # key = node name, value = strength of relationship
    nodes_dict = defaultdict(lambda: 0)
    for cur_name in node_names:
        try:
            cur_neighbors = kg.graph.neighbors(cur_name)
        except NetworkXError as err:
            if 'not in the graph' in str(err).lower():
                continue
            else:
                raise err

        for nbr in cur_neighbors:
            nodes_dict[nbr] += 1

    return nodes_dict


def iterate_graph(kg, start_words, max_hops=5):
    """
    arg: start_words = list of strings to start searching graph with
    arg: max_hops = max breadth-first-search depth
    return: dict of visited nodes
        val = num times word was hit when traversing the graph
    """
    visited_dict = defaultdict(lambda: 0)
    next_dict = get_next_nodes(start_words)
    counter = 0

    while next_dict:
        counter += 1
        if counter > max_hops:
            break

        next_keys = [x for x in next_dict.keys()]
        for key in next_keys:
            if key in visited_dict:
                visited_dict[key] += next_dict[key]
                del next_dict[key]

        next_dict = get_next_nodes(kg, next_dict.keys())

    return visited_dict

