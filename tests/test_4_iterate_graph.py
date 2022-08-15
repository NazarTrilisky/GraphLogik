import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


def test_get_next_nodes():
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_parse_tree(kg, story)

    visited
    nodes = kg.get_next_nodes(['merchant'])
    assert(nodes == {'rich': 1, 'have': 1})


if __name__ == '__main__':
    test_get_next_nodes()
    print('passed')

#@TODO Step function to iterate concepts


