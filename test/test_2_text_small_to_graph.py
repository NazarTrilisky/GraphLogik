import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_subj_verb_obj


with open('test/files/beauty_and_the_beast_small.txt', 'r') as fh:
    story = fh.read()

kg = KnowledgeGraph()
text_to_graph_subj_verb_obj(kg, story)

kg.show()

