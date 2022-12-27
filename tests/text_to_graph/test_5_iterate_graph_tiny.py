import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.graph import KnowledgeGraph
from src.query import iterate_graph
from src.text_to_graph import text_to_graph_link_all


def test_iterate_graph_loop_tiny():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    start_words = ['merchant']
    visited_dict = iterate_graph(kg, start_words)
    assert len(visited_dict) >= 4
    assert 'rich' in ['_'.join(x.split('_')[:-1]) for x in visited_dict.keys()]


def test_iterate_graph_loop_no_infinite_loops():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    start_words = ['merchant']
    iterate_graph(kg, start_words, 9999999999999999999999)
    assert True


if __name__ == '__main__':
    test_iterate_graph_loop_tiny()
    test_iterate_graph_loop_no_infinite_loops()
    print('Passed')

