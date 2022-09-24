import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_text_to_graph_link_all(show_graph=False):
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()
    #story = 'being a man of sense, he spared no cost for their education, but gave them all kinds of masters.'

    #story = 'so that, as she grew up, she still went by the name of Beauty, which made her sisters very jealous.'

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)

    if show_graph:
        kg.show()  # for humans only

    #assert kg.graph
    #assert kg.graph.number_of_nodes() > 5
    #assert len(kg.graph.edges) > 5


if __name__ == '__main__':
    test_text_to_graph_link_all(True)
    print("Passed")
