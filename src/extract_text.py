import fitz
from docx import Document


def extract_text_from_pdf(uploaded_file):
    pdf_document = fitz.open(stream=uploaded_file.read(), filetype="pdf")

    text = ""
    for page in pdf_document:
        text = text + page.get_text()

    pdf_document.close()
    return text

def extract_text_from_docx(uploaded_file):
    docx_document = Document(uploaded_file)

    text = ""
    for paragraph in docx_document.paragraphs:
        text = text + paragraph.text + "\n"
    
    return text