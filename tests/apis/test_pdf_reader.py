import sys
sys.path.insert(0, '.')

from src.apis.pdf_to_text import get_text_from_pdf


def test_get_text_from_pdf_file():
    file_path = 'tests/files/EnronAnnualReport2000.pdf'
    txt       = get_text_from_pdf(file_path)

    assert len(txt) == 242571
    assert "Items impacting comparability" in txt


if __name__ == '__main__':
    test_get_text_from_pdf_file()
    print("Passed")

