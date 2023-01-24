import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_text_to_graph_one_sentence():
    kg = KnowledgeGraph()
    txt = ('There was once a very rich merchant, who had six children, '
           'three sons, and three daughters;')
    text_to_graph_link_all(kg, txt)
    #import pdb
    #pdb.set_trace()
    pass


def test_text_to_graph_link_all(show_graph=False):
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    if show_graph:
        kg.show()  # for humans only

    assert kg.graph
    assert len(kg.graph) > 5
    assert kg.num_edges > 5


if __name__ == '__main__':
    test_text_to_graph_one_sentence()
    #test_text_to_graph_link_all(True)
    print("Passed")
