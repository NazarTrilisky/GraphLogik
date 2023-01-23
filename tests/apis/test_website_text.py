
from os.path import exists as path_exists
import sys
sys.path.insert(0, '.')

from src.apis.pdf_to_text import get_text_from_pdf


#@Todo: code website text scraping API and test for it
def test_website_to_graph():
    url = "http://asfd"
    txt = "scrape_url"
    # txt -> graph


if __name__ == '__main__':
    test_website_to_graph()
    print("Passed")

