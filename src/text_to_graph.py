
from itertools import combinations

import spacy
from depronounize.depronounize import replace_pronouns
from src.graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')

SKIPPED_POS = ['ADP', 'CCONJ']
ACCEPTED_POS = ['ADJ', 'ADV', 'INTJ', 'NOUN', 'NUM'
                'PART', 'PRON', 'PROPN', 'VERB']


class Node:
    def __init__(self, token, parent=None):
        self.token = token
        self.parent = parent
        self.kids = []


def add_and_link_nodes(kg, tok1, tok2, edge_attrs):
    if (
        tok1.lemma_.lower() != tok2.lemma_.lower() and
        not tok1.is_punct and
        not tok2.is_punct and
        tok1.text.strip() and
        tok2.text.strip()
    ):
        t1 = tok1.text.lower()
        t2 = tok2.text.lower()
        kg.addNode(t1)
        kg.addNode(t2)
        kg.addEdge(t1, t2, **edge_attrs)


def build_tree_from_heads(kg, root_node):
    queue = [root_node]
    while queue:
        cur_node = queue.pop(0)
        for kid_tok in cur_node.token.children:
            kid_node = Node(kid_tok, parent=cur_node)
            cur_node.kids.append(kid_node)
            queue.append(kid_node)


def link_node_to_kids(kg, cur_node, child_nodes):
    """
    Don't link two verbs in a row
    Don't link parts of speech (POS) that do not matter
    arg: kg: instance of KnowledgeGraph class
    arg: cur_node: root node, instance of Node class
    arg: child_nodes: list of Node class instances
    """
    for child_node in child_nodes:
        if cur_node.token.pos_ in ['VERB', 'AUX']:
            toks_to_link = [n.token for n in child_nodes
                            if n.token.pos_ in ACCEPTED_POS
                            and n.token.pos_ not in ['VERB', 'AUX']]
            pairs = list(combinations(toks_to_link, 2))
            for pair in pairs:
                add_and_link_nodes(kg, pair[0], pair[1],
                                   {'name': cur_node.token.text})

        elif (cur_node.token.pos_ in ACCEPTED_POS and
              child_node.token.pos_ in ACCEPTED_POS):
            add_and_link_nodes(
                kg,
                cur_node.token,
                child_node.token,
                {'name': ''}
            )

        elif child_node.token.pos_ in SKIPPED_POS:
            if child_node.kids:
                link_node_to_kids(kg, cur_node, child_node.kids)

        if child_node.kids:
            link_node_to_kids(kg, child_node, child_node.kids)


def text_to_graph_link_all(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    text = replace_pronouns(text)
    doc  = nlp(text)
    for sentence in doc.sents:
        root_node = Node(sentence.root)
        build_tree_from_heads(kg, root_node)
        link_node_to_kids(kg, root_node, root_node.kids)

