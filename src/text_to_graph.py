
import spacy

from src.graph import KnowledgeGraph
from src.pronouns import update_last_noun, get_text_for_pronoun


nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']


def add_and_link_nodes(kg, tok1, tok2):
    kg.addNode(tok1.lemma_)
    kg.addNode(tok2.lemma_)

    weight = 1
    edge = kg.graph.get_edge_data(tok1.lemma_, tok2.lemma_)
    if edge:
        weight += edge['weight']

    kg.addEdge(tok1.lemma_, tok2.lemma_, weight=weight)


def text_to_graph_parse_tree(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    Uses the approach of parse tree
    """
    new_text = text.replace(';', '.')
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens = nlp(sentence)
        accepted_pos = ['NOUN', 'VERB', 'ADJ']
        bypassed_lemmas = ['be']  # link two nodes directly: no "be" inbetween
        queue = [tok for tok in tokens if tok.dep_ == 'ROOT']

        def process_child_token(parent_token, token):
            child_tokens = [token]
            if token.lemma_ in bypassed_lemmas:
                child_tokens = [t for t in token.lefts]
                child_tokens += [t for t in token.rights]
            for c_tok in child_tokens:
                queue.append(c_tok)
                if (token.pos_ in accepted_pos and token.text.strip() and
                    parent_token.lemma_ != token.lemma_ and
                    token.lemma_ not in bypassed_lemmas and
                    parent_token.lemma_ not in bypassed_lemmas):
                    add_and_link_nodes(kg, parent_token, token)

        while queue:
            parent_token = queue.pop(0)
            for token in parent_token.lefts:
                process_child_token(parent_token, token)
            for token in parent_token.rights:
                process_child_token(parent_token, token)

