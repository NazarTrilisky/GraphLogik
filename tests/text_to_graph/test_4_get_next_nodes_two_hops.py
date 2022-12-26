import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all
from src.query import get_next_nodes


def test_iterate_graph():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    # first hop
    # key: node name, val: num times node hit
    visited_dict = defaultdict(lambda: 0)
    next_dict = get_next_nodes(kg, ['merchant'])

    for key in next_dict:
        visited_dict[key] += next_dict[key]

    assert len(visited_dict) == 4
    assert len(next_dict) == 4

    # second hop
    third_dict = get_next_nodes(kg, list(next_dict.keys()))
    assert len(third_dict) == 7
    assert third_dict['merchant'] == 4


if __name__ == '__main__':
    test_iterate_graph()
    print('passed')

