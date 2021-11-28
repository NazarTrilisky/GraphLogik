
import spacy
from src.graph import KnowledgeGraph

nlp = spacy.load('en_core_web_sm')


def translate_text_into_graph(kg, sentence):
    """
    Adds nodes and relationships from the sentence into knowledge graph (kg)
    """
    tokens = nlp(sentence)
    adj_list = []
    subj = None
    obj = None
    verb = None
    for token in tokens:
        if token.pos_ in [u'NOUN', u'PROPN']:
            kg.addNode(token.text)
            if adj_list:
                for adj in adj_list:
                    kg.connect(adj, token.text)
                adj_list.clear()

            if not verb:  #token.dep_.endswith('subj'):
                subj = token.text
            elif token.dep_.endswith('obj') and subj and verb:
                obj = token.text
                kg.connect(subj, verb, 1)
                kg.connect(verb, obj, 1)
        elif token.pos_ == u'PRON':
            # replace pronoun w. noun
            pass
        elif token.pos_ == u'ADJ':
            kg.addNode(token.text)
            adj_list.append(token.text)
        elif token.pos_ == u'VERB':
            kg.addNode(token.text)
            verb = token.text
        else:
            pass


if __name__ == '__main__':
    kg = KnowledgeGraph()
    text = "The quick brown fox jumped over the lazy, fat dog."
    translate_text_into_graph(kg, text)
    kg.show()

