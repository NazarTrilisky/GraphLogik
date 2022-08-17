import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


def test_text_to_graph_parse_tree_small_text(show_graph=False):
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_parse_tree(kg, story)

    if show_graph:
        kg.show()  # for humans

    assert kg.graph
    assert kg.graph.number_of_nodes() == 140
    assert len(kg.graph.edges) == 144


if __name__ == '__main__':
    test_text_to_graph_parse_tree_small_text(True)

