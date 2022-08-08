import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


with open('test/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
    story = fh.read()

kg = KnowledgeGraph()
text_to_graph_parse_tree(kg, story)

g = kg.graph

import pdb
pdb.set_trace()


#@TODO Input to activate nodes
#@TODO Step function to iterate concepts
#@TODO Output translate result

