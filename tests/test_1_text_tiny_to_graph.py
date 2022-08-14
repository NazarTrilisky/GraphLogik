import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


def test_text_to_graph_parse_tree(show_graph=False):
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_parse_tree(kg, story)

    if show_graph:
        kg.show()  # for humans only

    assert kg.graph
    assert kg.graph.number_of_nodes() == 29
    assert len(kg.graph.edges) == 21


if __name__ == '__main__':
    test_text_to_graph_parse_tree(True)

