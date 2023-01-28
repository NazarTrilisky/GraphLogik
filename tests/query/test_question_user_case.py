
# Sample use-case for querying next concept:
# ask a simple question and seek answer in visited_nodes.

import sys
sys.path.insert(0, '.')

from src.query import iterate_graph
from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_iterate_graph_loop_use_case():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    start_text = "Why were the sisters jealous?"
    start_words = start_text.split()
    visited_dict = iterate_graph(kg, start_words, max_hops=10)
    sorted_dict = dict(sorted(visited_dict.items(),
                              key=lambda x: x[1],
                              reverse=True))
    visited_list = [x[0] for x in sorted_dict.items()]
    assert len(visited_list) >= 5
    assert 'Beauty' in visited_list[:4]


if __name__ == '__main__':
    test_iterate_graph_loop_use_case()
    print("Passed")

