
import spacy
import networkx as nx


nlp = spacy.load('en_core_web_sm')
doc = nlp("The quick brown fox jumped over the lazy, fat dog.")

tokens = [t for t in doc]
for token in tokens:
    print("{} - {}, ".format(token.text, token.pos))


G = nx.Graph()
G.add_node(1)
print(G)

