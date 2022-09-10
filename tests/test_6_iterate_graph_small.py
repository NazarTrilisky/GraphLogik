import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_iterate_graph_loop_small():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    start_words = ['merchant']
    visited_dict = kg.iterate_graph(start_words)
    assert len(visited_dict) > 30
    assert visited_dict['merchant'] >= 5


def test_iterate_graph_loop_no_infinite_loops():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    start_words = ['merchant']
    kg.iterate_graph(start_words, 9999999999999999999999)
    assert True



if __name__ == '__main__':
    test_iterate_graph_loop_small()
    test_iterate_graph_loop_no_infinite_loops()
    print('Passed')

