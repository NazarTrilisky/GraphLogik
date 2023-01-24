import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_text_to_graph_link_all_small_text(show_graph=False):
    with open('tests/files/beauty_and_the_beast_small.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    if show_graph:
        kg.show()  # for humans

    assert kg.graph
    assert len(kg.graph) > 20
    assert kg.num_edges > 20


if __name__ == '__main__':
    test_text_to_graph_link_all_small_text(True)
    print("Passed")

