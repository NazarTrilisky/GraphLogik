
import spacy
from collections import defaultdict

from depronounize.depronounize import replace_pronouns
from src.graph import KnowledgeGraph, DEFAULT_WEIGHT


nlp = spacy.load('en_core_web_sm')

IGNORED_POS = ['PUNCT', 'SPACE']
NODE_POS    = ['NOUN', 'PRON', 'PROPN']
LEARN_STEP  = 1

# add int to ensure unique node names
name_count_dict = defaultdict(lambda: 0)


def build_tree_from_heads(kg, root_tok):
    queue = [root_tok]
    while queue:
        cur_tok = queue.pop(0)
        for kid_tok in cur_tok.children:
            queue.append(kid_tok)
            add_and_link_nodes(kg, cur_tok, kid_tok)


def add_and_link_nodes(kg, tok1, tok2):
    t1_txt = tok1.text.strip()
    t2_txt = tok2.text.strip()
    if (tok1.pos_ not in IGNORED_POS and tok2.pos_ not in IGNORED_POS
        and t1_txt and t2_txt):
        name1 = checkAndAddNode(kg, tok1)
        name2 = checkAndAddNode(kg, tok2)
        # rerunning neural paths is strengthening the connections
        if name1 != name2:
            if kg.edgeExists(name1, name2):
                kg.nodes[name1].edges[name2] += LEARN_STEP
                kg.nodes[name2].edges[name1] += LEARN_STEP
            else:
                kg.addEdge(name1, name2, weight=DEFAULT_WEIGHT)


def checkAndAddNode(kg, tok):
    name = tok.text
    if tok.pos_ not in NODE_POS:
        name = name + "_" + str(name_count_dict[name])
        name_count_dict[name] += 1

    kg.addNode(name, pos_=tok.pos_, dep_=tok.dep_)
    return name


def show_doc_dependency_tree(doc):
    from spacy import displacy
    displacy.serve(doc, style="dep")


def text_to_graph_link_all(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    text = text.replace(';', '.')
    text = replace_pronouns(text)
    doc  = nlp(text)

    for sentence in doc.sents:
        build_tree_from_heads(kg, sentence.root)

