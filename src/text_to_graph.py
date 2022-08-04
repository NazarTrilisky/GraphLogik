
import spacy
from src.graph import KnowledgeGraph

from src.pronouns import update_last_noun, get_text_for_pronoun


nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']


def add_adjectives_to_graph(kg, tokens):
    """
    Get entities and descriptions: adj expected to precede noun
    The 'tokens' arg is for a single sentence
    """
    descr_tokens = []
    for token in tokens:
        if token.pos_ in ['ADJ', 'NUM']:
            descr_tokens.append(token)
        elif token.pos_ in ['NOUN']:
            for descr_token in descr_tokens:
                if token.text.strip() and descr_token.text.strip():
                    kg.addNode(token.text.lower())
                    kg.addNode(descr_token.text.lower())
                    kg.addEdge(
                        token.text.lower(),
                        descr_token.text.lower(),
                        label='adj'
                    )
            descr_tokens.clear()


def get_subj_obj(tokens, idx):
    """
    Return tuple with two lists ([subjects], [objects])
    for the verb at the given index
    """
    subjects = []
    objects = []
    cur = idx - 1

    # move backwards to find subjects
    while cur >= 0 and tokens[cur].dep_ != 'VERB':
        if tokens[cur].dep_.endswith('subj') and tokens[cur].text.strip():
            subjects.append(tokens[cur])
        cur -= 1

    # move forward to find objects
    cur = idx + 1
    while cur < len(tokens) and tokens[cur].dep_ != 'VERB':
        if tokens[cur].dep_.endswith('obj') and tokens[cur].text.strip():
            objects.append(tokens[cur])
        cur += 1

    return (subjects, objects)


def get_token_text(token):
    if token.pos_ == 'PRON':
        return get_text_for_pronoun(token).lower()
    return token.text.lower()


def text_to_graph_subj_verb_obj(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    Uses the approach of adding a verb and it's subject(s) and object(s)
    """
    new_text = text.replace(';', '.')
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens_w_stopwords = nlp(sentence)

        tokens = [token for token in tokens_w_stopwords if not token.text in stopwords]
        tokens = [token for token in tokens if token.text.strip()]

        # Add adjectives to nouns
        add_adjectives_to_graph(kg, tokens)

        # Add subj-verb-obj triples
        for idx in range(len(tokens)):
            token = tokens[idx]
            if tokens[idx].pos_ == 'NOUN':
                update_last_noun(tokens, idx)
            elif token.pos_ == 'VERB':
                verb_token = token
                subjects, objects = get_subj_obj(tokens, idx)

                if subjects and objects:
                    for subj in subjects:
                        for obj in objects:
                            subj_text = get_token_text(subj)
                            obj_text = get_token_text(obj)
                            if subj_text.lower() != obj_text.lower():
                                kg.addNode(subj_text)
                                kg.addNode(obj_text)
                                kg.addEdge(
                                    get_token_text(subj),
                                    get_token_text(obj),
                                    label=verb_token.text
                                )

                elif subjects and not objects:
                    print(subjects)

                elif objects and not subjects:
                    print(objects)


def add_and_link_nodes(kg, tok1, tok2):
    kg.addNode(tok1.lemma_)
    kg.addNode(tok2.lemma_)
    kg.addEdge(tok1.lemma_, tok2.lemma_)



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
                if (token.pos_ in accepted_pos and token.text and
                    parent_token.lemma_ != token.lemma_ and
                    token.lemma_ not in bypassed_lemmas):
                    add_and_link_nodes(kg, parent_token, token)

        while queue:
            parent_token = queue.pop(0)
            for token in parent_token.lefts:
                process_child_token(parent_token, token)
            for token in parent_token.rights:
                process_child_token(parent_token, token)

