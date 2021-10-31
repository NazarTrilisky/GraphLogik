
import spacy
from graph import KnowledgeGraph

nlp = spacy.load('en_core_web_sm')
kg = KnowledgeGraph()
tokens = nlp("The quick brown fox jumped over the lazy, fat dog.")


def link_related_nodes(kg, token_idx):
    """ Link adjectives and verbs and subj/obj """
    if tokens[token_idx].pos_ in [u'NOUN', u'PROPN']:
        # go backwards
        for idx in range(token_idx-1, -1, -1):
            if tokens[idx].pos_ in [u'ADJ', u'advcl', u'VERB']:
                kg.connect(tokens[token_idx].text, tokens[idx].text, weight=1)

        # go forwards
        for idx in range(token_idx+1, 1, len(tokens)):
            if tokens[idx].pos_ in [u'VERB']:
                kg.connect(tokens[token_idx].text, tokens[idx].text, weight=1)


# Add all nodes
for token in tokens:
    #@TODO check u'obj' / subj in token.dep_
    print("%s, %s, %s" % (token.text, token.pos_, token))
    if token.pos_ in [u'NOUN', u'PROPN']:
        kg.addNode(token.text)
    elif token.pos_ == u'PRON':
        #@TODO replace pronoun w. noun
        pass
    elif token.pos_ == u'ADJ':
        kg.addNode(token.text)
        #kg.connect(
    elif token.pos_ == u'VERB':
        kg.addNode(token.text)
    else:
        #@TODO handle case
        pass


# Link nodes
for idx in range(len(tokens)):
    link_related_nodes(kg, idx)


kg.show()

