
import spacy
from src.graph import KnowledgeGraph

nlp = spacy.load('en_core_web_sm')
stopwords = nlp.Defaults.stop_words


def translate_text_into_graph(kg, sentences):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    #@TODO replace_pronouns(sentences)
    for sentence in sentences:
        tokens_w_stopwords = nlp(sentence)
        tokens = [word for word in tokens_w_stopwords if not word in stopwords]
        adj_list = []
        subj = None
        obj = None
        verb = None
        for token in tokens:
            if token.pos_ in [u'NOUN', u'PROPN']:
                kg.addNode(token.text)
                if adj_list:
                    for adj in adj_list:
                        kg.connect(adj, token.lemma_)
                    adj_list.clear()

                if not verb:  #token.dep_.endswith('subj'):
                    subj = token.lemma_
                elif token.dep_.endswith('obj') and subj and verb:
                    obj = token.lemma_
                    kg.connect(subj, verb, 1)
                    kg.connect(verb, obj, 1)
            elif token.pos_ == u'PRON':
                # replace pronoun w. noun
                pass
            elif token.pos_ == u'ADJ':
                kg.addNode(token.lemma_)
                adj_list.append(token.lemma_)
            elif token.pos_ == u'VERB':
                kg.addNode(token.lemma_)
                verb = token.lemma_
            else:
                pass


if __name__ == '__main__':
    kg = KnowledgeGraph()
    text = "The quick brown fox jumped over the lazy, fat dog."
    translate_text_into_graph(kg, text)
    kg.show()

