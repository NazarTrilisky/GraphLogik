import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


with open('test/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
    story = fh.read()

kg = KnowledgeGraph()
text_to_graph_parse_tree(kg, story)

neighbors = kg.get_neighbors('merchant')
print(neighbors)

#@TODO Input to activate nodes
#@TODO Step function to iterate concepts
#@TODO Output translate result

