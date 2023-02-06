
import os
import sys
import pathlib
import warnings
warnings.filterwarnings("ignore")

sys.path.insert(0, '.')
from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all
from src.graph_algos import bfs
from src.apis.pdf_to_text import get_text_from_pdf


def test_bfs_berkshire_vs_enron():
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

    #@todo check combinations and patterns in best & worst
    #SEARCH_LIST = ['compliance', 'earnings', 'sustainable']
    SEARCH_LIST = ["debt", "borrow"]
    SEARCH_LIST = ['loss', 'losses']

    # Possible approach
    # Find key concepts that relate to loss or debt or compliance
    # Determine the nature of the relationship
    # Summarize sentiment, word2vec, fuzzy summary of how debt, loss, ... is handled


    # Some of most successful companies in 2000:
    # General Electric, Exxon Mobil, Ford, Citigroup, WalMart, Bank of America
    # CocaCola

    # Some of least successful companies in 2000:
    # America Online, WorldCom, Kmart, Global Crossing, Pacific Gas & Electric Co.
    # Lehman Brothers, Chrysler


    def print_visited(kg_obj):
        visited_dict = bfs.breadth_first_search(kg_obj, SEARCH_LIST, max_depth=3)
        top_nodes = [(k, v) for k, v in sorted(visited_dict.items(),
                     key=lambda item: item[1], reverse=True)]
        for x in top_nodes[:15]:
            print(x)

    print("---------------------\nEnron:")
    print_visited(e_kg)
    print("---------------------\nBerkshire:")
    print_visited(b_kg)


if __name__ == '__main__':
    test_bfs_berkshire_vs_enron()
    print('passed')
