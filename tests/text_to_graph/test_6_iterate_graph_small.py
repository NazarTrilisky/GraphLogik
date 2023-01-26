import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.query import iterate_graph
from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_iterate_graph_loop_small():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    start_words = ['merchant']
    visited_dict = iterate_graph(kg, start_words)
    print(len(visited_dict))
    assert len(visited_dict) > 5


if __name__ == '__main__':
    test_iterate_graph_loop_small()
    print('Passed')

