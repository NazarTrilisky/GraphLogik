
import spacy

from src.visualizer import DisplayGraph


def breadth_first_search(kg, start_words, max_depth):
    """
    arg: start_words = list of strings to start searching graph with
    arg: max_depth = max breadth-first-search depth
    return: dict of visited nodes
        key = node name, val = strength of path to that node
    """
    IGNORED_POS = ['ADP', 'DET', 'CCONJ']
    POS_TO_DISPLAY = ['NOUN']
    STEP_WEIGHT_SUBTRACTION = 1

    depth = 0
    dgr = DisplayGraph()
    # tuple (node-name, sum-of-edge-weights-to-node-from-start-words)
    queue = [(word, 1) for word in start_words]
    # key = word, val = sum of edge weights to node
    visited_dict = {k:0 for k in start_words}

    while queue and depth < max_depth:
        depth += 1
        cur_word, cur_weight = queue.pop(0)
        if cur_word in kg.nodes:
            dgr.addNode(cur_word)
            for neighbor_word in kg.nodes[cur_word].edges.keys():
                if neighbor_word not in visited_dict:
                    queue.append((neighbor_word,
                                  kg.nodes[cur_word].edges[neighbor_word]
                                  + cur_weight
                                  - STEP_WEIGHT_SUBTRACTION))
                    if kg.nodes[neighbor_word].attrs['pos_'] not in IGNORED_POS:
                        visited_dict[neighbor_word] = kg.nodes[cur_word].edges[neighbor_word]
                if kg.nodes[neighbor_word].attrs['pos_'] in POS_TO_DISPLAY:
                    dgr.addNode(neighbor_word)
                    dgr.addEdge(cur_word, neighbor_word)

    dgr.show()

    return visited_dict

