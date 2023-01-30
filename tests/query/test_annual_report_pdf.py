import sys
sys.path.insert(0, '.')

from collections import defaultdict

from src.graph import KnowledgeGraph
from src.text_to_graph import text_to_graph_link_all
from src.query import get_next_nodes
from src.apis.pdf_to_text import get_text_from_pdf


def test_annual_report_iterate():
    file_path = 'tests/files/EnronAnnualReport2000.pdf'
    pdf_txt   = get_text_from_pdf(file_path)

    kg = KnowledgeGraph()
    text_to_graph_link_all(kg, pdf_txt)

    # first hop
    visited_dict = defaultdict(lambda: 0)
    next_dict = get_next_nodes(kg, 'purchase')
    assert len(next_dict) > 15
    assert 'contracts' in next_dict.keys()


if __name__ == '__main__':
    test_annual_report_iterate()
    print('passed')

