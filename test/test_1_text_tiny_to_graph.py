import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_parse_tree


#with open('test/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
#    story = fh.read()

story = "There was once a very rich merchant, who had six children, three sons, and three daughters;"

kg = KnowledgeGraph()
text_to_graph_parse_tree(kg, story)

kg.show()

