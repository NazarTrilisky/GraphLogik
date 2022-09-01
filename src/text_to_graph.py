
import spacy

from src.graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']


def add_and_link_nodes(kg, tok1, tok2, edge_attrs):
    kg.addNode(tok1.lemma_)
    kg.addNode(tok2.lemma_)
    kg.addEdge(tok1.lemma_, tok2.lemma_, **edge_attrs)


def text_to_graph_parse_tree(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    Uses the approach of parse tree
    """
    new_text = text.replace(';', '.')
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens = nlp(sentence)
        accepted_pos = ['NOUN', 'ADJ']
        bypassed_pos = ['VERB']
        queue = [tok for tok in tokens if tok.dep_ == 'ROOT']

        def process_child_token(parent_token, token):
            child_tokens = [token]
            if token.pos_ in bypassed_pos:
                child_tokens = [t for t in token.lefts]
                child_tokens += [t for t in token.rights]

            print("%s ---- %s" % (parent_token, child_tokens))

            for c_tok in child_tokens:
                queue.append(c_tok)
                if (c_tok.pos_ in accepted_pos and
                    c_tok.text.strip() and
                    parent_token.text.strip() and
                    parent_token.lemma_ != c_tok.lemma_ and
                    token.lemma_ != c_tok.lemma_
                   ):
                    add_and_link_nodes(kg, parent_token, c_tok,
                                       {'name': token.lemma_})

        while queue:
            parent_token = queue.pop(0)
            for token in parent_token.lefts:
                process_child_token(parent_token, token)
            for token in parent_token.rights:
                process_child_token(parent_token, token)

