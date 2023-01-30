
from collections import defaultdict
import spacy

from src.visualizer import DisplayGraph


def get_next_nodes(kg, word):
    """
    arg: kg = KnowledgeGraph object
    arg: word = name of node to start with
    return: <dict-of-next-nodes>
        dict: key = next node name, val = num times node hit
    """
    # key = node name, value = strength of relationship
    nodes_dict = defaultdict(lambda: 0)
    if word in kg.nodes:
        for nbr in kg.nodes[word].edges.keys():
            #print("{} -- {} -- {}".format(nbr,
            #      kg.nodes[nbr].attrs['pos_'],
            #      kg.nodes[nbr].attrs['dep_']))
            nodes_dict[nbr] += kg.nodes[nbr].edges[word] - 1

    return nodes_dict


def iterate_graph(kg, start_words, max_hops=5):
    """
    arg: start_words = list of strings to start searching graph with
    arg: max_hops = max breadth-first-search depth
    return: dict of visited nodes
        key = node name, val = strength of path to that node
    """
    visited_dict = defaultdict(lambda: 0)
    counter = 0

    next_dict = {}
    for word in start_words:
        next_dict.update(get_next_nodes(kg, word))

    IGNORED_POS = ['ADP', 'DET']
    while next_dict and counter < max_hops:
        counter += 1
        for word in next_dict:
            if (word not in visited_dict and
                kg.nodes[word].attrs['pos_'] not in IGNORED_POS):
                visited_dict[word] = next_dict[word]

        words = list(next_dict.keys())
        next_dict = {}
        for word in words:
            next_dict.update(get_next_nodes(kg, word))

    return visited_dict

