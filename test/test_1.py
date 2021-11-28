import sys
sys.path.insert(0, '.')

from src.graph import KnowledgeGraph
from src.text_to_graph import translate_text_into_graph


with open('test/files/beauty_and_the_beast_tiny.txt', 'r') as fh:
    story = fh.read()

kg = KnowledgeGraph()
sentences = story.split('.')
for sentence in sentences:
    translate_text_into_graph(kg, story)

kg.show()

