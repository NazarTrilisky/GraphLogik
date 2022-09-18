
from itertools import combinations

import spacy
from depronounize.depronounize import replace_pronouns
from src.graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')

IGNORED_POS = ['PUNCT']
NODE_POS    = ['NOUN', 'PRON', 'PROPN']
ACTION_POS  = ['VERB', 'AUX']


class Node:
    def __init__(self, token, parent=None):
        self.token = token
        self.parent = parent
        self.kids = []
        self.visited = False


def add_and_link_nodes(kg, tok1, tok2, edge_attrs):
    if (
        tok1.lemma_.lower() != tok2.lemma_.lower() and
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


def link_to_upwards_node(kg, start_node):
    start_node.visited = True
    path_info = []
    if start_node.token.pos_ not in NODE_POS:
        path_info.append(start_node.token.text)

    # find next upwards node
    cur_node = start_node
    while (cur_node.parent and
           cur_node.parent.token.pos_ not in NODE_POS):
        cur_node = cur_node.parent
        path_info.append(cur_node.token.text)

    if cur_node.parent and cur_node.parent.token.pos_ in NODE_POS:
        if start_node.token.pos_ in NODE_POS:
            for edge_str in path_info:
                add_and_link_nodes(kg, start_node.token, cur_node.parent.token,
                                   {'label': edge_str})
        else:
            kg.addLabelToNode(cur_node.parent.token.text, str(path_info))


def bottom_up_node_connect(kg, root_node):
    stack = [root_node]
    while stack:
        cur_node = stack.pop(-1)
        for kid_node in cur_node.kids:
            stack.append(kid_node)
            if (kid_node.token.pos_ not in IGNORED_POS and not kid_node.visited):
                link_to_upwards_node(kg, kid_node)


def erase_me_please(kg, cur_node, child_nodes):
    for child_node in child_nodes:
        if cur_node.token.pos_ in ['VERB', 'AUX']:
            toks_to_link = [n.token for n in child_nodes]
            pairs = list(combinations(toks_to_link, 2))
            for pair in pairs:
                add_and_link_nodes(kg, pair[0], pair[1],
                                   {'label': cur_node.token.text})


def text_to_graph_link_all(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    text = replace_pronouns(text)
    doc  = nlp(text)
    #from spacy import displacy
    #displacy.serve(doc, style="dep")
    for sentence in doc.sents:
        root_node = Node(sentence.root)
        build_tree_from_heads(kg, root_node)
        bottom_up_node_connect(kg, root_node)

