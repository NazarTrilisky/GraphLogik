import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import translate_text_into_graph


with open('test/files/beauty_and_the_beast_small.txt', 'r') as fh:
    story = fh.read()

kg = KnowledgeGraph()
translate_text_into_graph(kg, story)

#@TODO Input to activate nodes
#@TODO Step function to iterate concepts
#@TODO Output translate result

