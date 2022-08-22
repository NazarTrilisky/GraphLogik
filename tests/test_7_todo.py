#@TODO Output translate result
# sample use-case for querying next concept
# E.g. ask a simple question and seek answer in visited_nodes

import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


def test_iterate_graph_loop_use_case():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_parse_tree(kg, story)

    start_text = "Why were the sisters jealous?"
    start_words = start_text.split()
    print(start_words)
    visited_dict = kg.iterate_graph(start_words, max_hops=10)
    sorted_dict = dict(sorted(visited_dict.items(),
                              key=lambda x: x[1],
                              reverse=True))
    print(sorted_dict)


if __name__ == '__main__':
    test_iterate_graph_loop_use_case()
    print("Passed")

