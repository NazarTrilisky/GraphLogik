
from collections import defaultdict
import spacy


def get_next_nodes(kg, node_names):
    """
    arg: kg = KnowledgeGraph object
    arg: node_names = list of strings
    return: <dict-of-next-nodes>
        dict: key = next node name, val = num times node hit
    """

    #@todo tests
    # 1. Ignore unimportant parts of speech
    # 2. Don't visit same nodes > once

    # key = node name, value = strength of relationship
    nodes_dict = defaultdict(lambda: 0)
    for cur_name in node_names:
        if cur_name in kg.nodes:
            for nbr in kg.nodes[cur_name].edges.keys():
                #print("{} -- {} -- {}".format(cur_name,
                #      kg.nodes[cur_name].attrs['pos_'],
                #      kg.nodes[cur_name].attrs['dep_']))
                nodes_dict[nbr] += kg.nodes[cur_name].edges[nbr] - 1

    return nodes_dict


def iterate_graph(kg, start_words, max_hops=5):
    """
    arg: start_words = list of strings to start searching graph with
    arg: max_hops = max breadth-first-search depth
    return: dict of visited nodes
        key = node name, val = num times node visited during traversal
    """
    visited_dict = defaultdict(lambda: 0)
    next_dict = get_next_nodes(kg, start_words)
    counter = 0

    IGNORED_POS = ['ADP']

    while next_dict and counter < max_hops:
        counter += 1
        for nxt_nd in next_dict:
            if (nxt_nd not in visited_dict and
                kg.nodes[nxt_nd].attrs['pos_'] not in IGNORED_POS):
                visited_dict[nxt_nd] = next_dict[nxt_nd]
        next_dict = get_next_nodes(kg, list(next_dict.keys()))

    return visited_dict

