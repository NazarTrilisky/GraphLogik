import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


def test_iterate_graph_loop():
    # Step function to iterate concepts
    with open('tests/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
        story = fh.read()

    kg = KnowledgeGraph()
    text_to_graph_parse_tree(kg, story)

    start_words = ['merchant']

    # key: node lemma, val: num times node hit
    visited_dict = defaultdict(lambda: 0)
    cur_lemmas, next_dict = kg.get_next_nodes(start_words)

    counter = 0

    while next_dict:
        counter += 1
        if counter > 999:
            raise Exception("Infinite loop")

        for cur_lemma in cur_lemmas:
            visited_dict[cur_lemma] += 1

        for key in next_dict:
            if key in visited_dict:
                visited_dict[key] += next_dict[key]
                del next_dict[key]



if __name__ == '__main__':
    test_iterate_graph_loop()
    print('passed')

