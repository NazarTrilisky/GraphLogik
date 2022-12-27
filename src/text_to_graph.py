
import spacy
from collections import defaultdict

from depronounize.depronounize import replace_pronouns
from src.graph import KnowledgeGraph


nlp = spacy.load('en_core_web_sm')

IGNORED_POS = ['PUNCT', 'SPACE']
NODE_POS    = ['NOUN', 'PRON', 'PROPN']

# add int to ensure unique node names
name_count_dict = defaultdict(lambda: 0)


class Node:
    def __init__(self, token):
        self.token      = token
        self.kids       = []
        self.dep_       = token.dep_
        self.pos_       = token.pos_
        self.text       = token.text
        self.name       = token.text
        if token.pos_ not in NODE_POS:
            self.name   = token.text + "_" + str(name_count_dict[token.text])
            name_count_dict[token.text] += 1


def build_tree_from_heads(kg, root_node):
    queue = [root_node]
    while queue:
        cur_node = queue.pop(0)
        for kid_tok in cur_node.token.children:
            kid_node = Node(kid_tok)
            cur_node.kids.append(kid_node)
            queue.append(kid_node)


def addConnectorNode(kg, name):
    unique_name = name + "_" + str(name_count_dict[name])
    kg.addNode(unique_name)
    name_count_dict[name] += 1
    return unique_name


def add_all_nodes_to_graph(kg, root_node):
    queue = [root_node]
    while queue:
        cur_node = queue.pop(0)
        for kid_node in cur_node.kids:
            queue.append(kid_node)
            if (cur_node.pos_ not in IGNORED_POS and
                kid_node.pos_ not in IGNORED_POS and
                cur_node.text.strip() and
                kid_node.text.strip()):
                kg.addNode(kid_node.name)
                kg.addNode(cur_node.name)
                edge_data = kg.graph.get_edge_data(kid_node.name,
                                                   cur_node.name)
                # rerunning neural paths is strengthening the connections
                if edge_data: # edge already exists
                    kg.graph[kid_node.name][cur_node.name]['weight'] += 1
                else:
                    kg.addEdge(cur_node.name, kid_node.name, weight=1)


def text_to_graph_link_all(kg, text):
    """
    Adds nodes and relationships from the sentences into knowledge graph (kg)
    """
    text = text.replace(';', '.')
    text = replace_pronouns(text)
    doc  = nlp(text)
    #from spacy import displacy
    #displacy.serve(doc, style="dep")
    for sentence in doc.sents:
        root_node = Node(sentence.root)
        build_tree_from_heads(kg, root_node)
        add_all_nodes_to_graph(kg, root_node)

