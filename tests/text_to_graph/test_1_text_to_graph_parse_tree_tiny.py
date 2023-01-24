import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_text_to_graph_one_sentence():
    kg = KnowledgeGraph()
    txt = ('There was once a very rich merchant, who had six children, '
           'three sons, and three daughters;')
    text_to_graph_link_all(kg, txt)
    assert len(kg.nodes) == 14
    assert kg.num_edges == 15
    assert not kg.nodes['merchant'].attrs
    assert len(kg.nodes['merchant'].edges) == 4
    for node_name in ['was_0', 'a_0', 'rich_0', 'had_0']:
        assert node_name in kg.nodes
    kg.updateNodeAttrs('merchant', net_worth=100000, age=59)
    assert len(kg.nodes['merchant'].attrs) == 2
    assert kg.nodes['merchant'].attrs['net_worth'] == 100000
    assert kg.nodes['merchant'].attrs['age'] == 59
    assert len(kg.nodes['merchant'].edges) == 4


def test_text_to_graph_link_all(show_graph=False):
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    if show_graph:
        kg.show()  # for humans only

    assert kg.nodes
    assert len(kg.nodes) == 53
    assert kg.num_edges == 69


if __name__ == '__main__':
    test_text_to_graph_one_sentence()
    test_text_to_graph_link_all()
    print("Passed")

