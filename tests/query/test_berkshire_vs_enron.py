
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

    enron_path = os.path.join(test_file_path, 'EnronAnnualReport2000.pdf')
    berkshire_path = os.path.join(test_file_path, 'BerkshireHathawayAnnualReport2000.pdf')

    #@todo finish test


if __name__ == '__main__':
    test_berkshire_vs_enron()
    print('passed')

