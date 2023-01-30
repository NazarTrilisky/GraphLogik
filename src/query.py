
from collections import defaultdict
import spacy

from src.visualizer import DisplayGraph


#@todo: baseline is bershire graph: compare how enron relations stand out
# idea: find how differently enron treated debt and losses compared to berkshire
# by looking at debt/loss relationships with other concepts (earnings, transparency, etc.)
# Preferably expand this to 10+ successful and unsuccessful company annual reports

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

    #@todo remove DisplayGraph code
    dgr = DisplayGraph()
    TO_DISPLAY_POS = ['NOUN']

    next_dict = {k:1 for k in start_words}
    IGNORED_POS = ['ADP', 'DET']

    while next_dict and counter < max_hops:
        counter += 1
        new_next_dict = {}
        for word in next_dict:
            if (word not in visited_dict and
                kg.nodes[word].attrs['pos_'] not in IGNORED_POS):
                visited_dict[word] = next_dict[word]
                nxt_dict = get_next_nodes(kg, word)
                for next_word in nxt_dict:
                    new_next_dict[next_word] = nxt_dict[next_word]
                    dgr.addNode(word)
                    dgr.addNode(next_word)
                    dgr.addEdge(word, next_word)

        next_dict = new_next_dict

    #dgr.show()  #@todo uncomment for testing annual reports again

    return visited_dict

