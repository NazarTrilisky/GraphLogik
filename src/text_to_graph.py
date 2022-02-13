
import spacy
from src.graph import KnowledgeGraph

from depronounize.depronounize import replace_pronouns

nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']


def translate_text_into_graph(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    new_text = replace_pronouns(text)
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens_w_stopwords = nlp(sentence)
        tokens = [token for token in tokens_w_stopwords if not token.text in stopwords]
        adj_list = []
        subj = None
        obj = None
        verb = None

        # get entities and descriptions: adj expected to precede noun
        descr_tokens = []
        for token in tokens:
            if token.pos_ in ['ADJ', 'NUM']:
                descr_tokens.append(token)
            elif token.pos_ in ['NOUN']:
                kg.addNode(token.lemma_)
                for descr_token in descr_tokens:
                    kg.addNode(descr_token.lemma_)
                    kg.connect(token.lemma_, descr_token.lemma_)
                descr_tokens.clear()

        # get root verb and connect main action, subj, obj
        subj_tok = []
        obj_tok = []
        verb_tok = None
        for token in tokens:
            if token.dep_ == 'ROOT':
                verb_tok = token
            elif token.dep_.endswith('subj'):
                subj_tok.append(token)
            elif token.dep_.endswith('obj'):
                obj_tok.append(token)

        if verb_tok:
            kg.addNode(verb_tok.lemma_)
            for st in subj_tok:
                kg.addNode(st.lemma_)
                kg.connect(st.lemma_, verb_tok.lemma_)
            for ot in obj_tok:
                kg.addNode(ot.lemma_)
                kg.connect(ot.lemma_, verb_tok.lemma_)


if __name__ == '__main__':
    kg = KnowledgeGraph()
    text = "The quick brown fox jumped over the lazy, fat dog."
    translate_text_into_graph(kg, text)
    kg.show()

