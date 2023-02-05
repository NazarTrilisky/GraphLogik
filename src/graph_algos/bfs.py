
from collections import defaultdict
import spacy

from src.visualizer import DisplayGraph


def bfs(kg, start_words, max_depth):
    """
    arg: start_words = list of strings to start searching graph with
    arg: max_depth = max breadth-first-search depth
    return: dict of visited nodes
        key = node name, val = strength of path to that node
    """
    counter = 0
    dgr = DisplayGraph()
    TO_DISPLAY_POS = ['NOUN']

    next_dict = {k:1 for k in start_words}
    visited_dict = {k:1 for k in start_words}
    IGNORED_POS = ['ADP', 'DET']

    while next_dict and counter < max_depth:
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

    for key in next_dict:
        visited_dict[key] = next_dict[key]


    #dgr.show()

    return visited_dict

