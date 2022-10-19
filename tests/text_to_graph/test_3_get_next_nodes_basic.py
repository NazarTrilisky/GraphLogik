import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_get_next_nodes():
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    cur_lemmas, next_nodes = kg.get_next_nodes(['merchant'])
    next_node_names = ['_'.join(x.split('_')[:-1]) for x in next_nodes.keys()]
    assert 'rich' in next_node_names
    assert cur_lemmas == ['merchant']


if __name__ == '__main__':
    test_get_next_nodes()
    print('Passed')

