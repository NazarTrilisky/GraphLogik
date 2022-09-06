
import spacy
from depronounize.depronounize import replace_pronouns
from src.graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')
stopwords = ['a', 'the', 'for', 'at', 'by']


def add_and_link_nodes(kg, tok1, tok2, edge_attrs):
    #accepted_pos = ['VERB', 'NOUN', 'ADJ', 'NUM', 'DET']
    if (
        tok1.lemma_.lower() != tok2.lemma_.lower() and
        not tok1.is_punct and
        not tok2.is_punct and
        tok1.text.strip() and
        tok2.text.strip()
    ):
        kg.addNode(tok1.lemma_.lower())
        kg.addNode(tok2.lemma_.lower())
        kg.addEdge(tok1.lemma_.lower(),
                   tok2.lemma_.lower(),
                   **edge_attrs)


def process_verb(kg, verb_token):
    subj = []
    obj = []
    for t2 in verb_token.subtree:
        if t2.pos_ in ['VERB', 'AUX'] and verb_token.lemma_ != t2.lemma_:
            process_verb(kg, t2)
        elif 'subj' in t2.dep_:
            for t3 in t2.subtree:
                subj.append(t3)
        elif 'obj' in t2.dep_:
            for t3 in t2.subtree:
                obj.append(t3)

    #print("\n   %s" % verb_token)
    #print("subj %s" % subj)
    #print("obj %s" % obj)

    if subj and obj:
        for s1 in subj:
            for o1 in obj:
                add_and_link_nodes(kg, s1, o1,
                                   {'name': verb_token.lemma_})
    elif subj:
        for s1 in subj:
            add_and_link_nodes(kg, s1, verb_token,
                                   {'name': 'action'})
    elif obj:
        for o1 in obj:
            add_and_link_nodes(kg, verb_token, o1,
                                   {'name': 'action'})


def build_tree_from_verb(kg, tok):
    visited = set()
    queue = [tok]
    while queue:
        cur = queue.pop(0)
        visited.add(cur.lemma_.lower())
        for t1 in cur.subtree:
            if t1.lemma_.lower() not in visited:
                if t1.pos_ in ['VERB', 'AUX']:
                    build_tree_from_verb(kg, t1)
                else:
                    queue.append(t1)

        if cur.has_head():
            add_and_link_nodes(kg, cur, cur.head, {'name': ''})



def text_to_graph_link_all(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    text = replace_pronouns(text)
    new_text = text.replace(';', '.')
    sentences = new_text.split(".")

    for sentence in sentences:
        tokens = nlp(sentence)
        for t1 in tokens:
            if t1.dep_ == 'ROOT':
                process_verb(kg, t1)

