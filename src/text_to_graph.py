
import spacy

from graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')


tokens = nlp("The quick brown fox jumped over the lazy, fat dog.")
for token in tokens:
    print("%s, %s, %s" % (token.text, token.pos_, token))


