import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all


def test_iterate_graph():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, story)


    # first hop
    # key: node lemma, val: num times node hit
    visited_dict = defaultdict(lambda: 0)
    cur_lemmas, next_dict = kg.get_next_nodes(['merchant'])

    for cur_lemma in cur_lemmas:
        visited_dict[cur_lemma] += 1

    for key in next_dict:
        if key in visited_dict:
            visited_dict[key] += next_dict[key]
            del next_dict[key]

    assert visited_dict == {'merchant': 1}
    assert next_dict == {'children': 1, 'there': 1, 'once': 1, 'rich': 1}


    # second hop
    second_lemmas, third_dict = kg.get_next_nodes(list(next_dict.keys()))
    assert second_lemmas == ['child', 'there', 'once', 'rich']
    assert third_dict == {'once': 1, 'merchant': 3, 'there': 1, 'very': 1}


if __name__ == '__main__':
    test_iterate_graph()
    print('passed')

