
from PyPDF2 import PdfReader


def get_text_from_pdf(file_path):
    full_txt = ""
    reader = PdfReader(file_path)
    for page in reader.pages:
        full_txt += "\n" + page.extract_text()
    return full_txt

