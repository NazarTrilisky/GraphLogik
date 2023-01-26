
import os
import sys
import pathlib

from collections import defaultdict

sys.path.insert(0, '.')
from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all
from src.query import get_next_nodes
from src.apis.pdf_to_text import get_text_from_pdf


#@todo update to use graph db
def test_berkshire_vs_enron():
    test_file_path = pathlib.Path(__file__).parents[1].resolve()
    test_file_path = os.path.join(test_file_path, 'files')

    e_pkl_path = os.path.join(test_file_path, 'enron_2000_graph.pkl')
    b_pkl_path = os.path.join(test_file_path, 'berkshire_2000_graph.pkl')

    if os.path.exists(e_pkl_path):
        e_kg = KnowledgeGraph.load_graph(e_pkl_path)
    else:
        enron_path = os.path.join(test_file_path, 'EnronAnnualReport2000.pdf')
        e_txt = get_text_from_pdf(enron_path)
        e_kg = KnowledgeGraph()
        text_to_graph_link_all(e_kg, e_txt)
        e_kg.save_graph(e_pkl_path)

    if os.path.exists(b_pkl_path):
        b_kg = KnowledgeGraph.load_graph(b_pkl_path)
    else:
        berkshire_path = os.path.join(test_file_path, 'BerkshireHathawayAnnualReport2000.pdf')
        b_txt = get_text_from_pdf(berkshire_path)
        b_kg = KnowledgeGraph()
        text_to_graph_link_all(b_kg, b_txt)
        b_kg.save_graph(b_pkl_path)

    # first hop
    visited_dict = defaultdict(lambda: 0)
    next_dict = get_next_nodes(e_kg, ['purchase'])

    #assert len(next_dict) > 15
    #assert 'contracts' in next_dict.keys()



    #@todo finish test


if __name__ == '__main__':
    test_berkshire_vs_enron()
    print('passed')

