import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


def test_iterate_graph():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_parse_tree(kg, story)

    visited = []
    cur_lemmas, nodes_dict = kg.get_next_nodes(['merchant'])
    visited += cur_lemmas
    next_dict = {key: nodes_dict[key] for key in nodes_dict
                 if key not in visited}


if __name__ == '__main__':
    test_iterate_graph()
    print('passed')

