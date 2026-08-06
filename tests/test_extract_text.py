from io import BytesIO

import fitz
from docx import Document

from src.extract_text import extract_text_from_docx, extract_text_from_pdf


def test_extract_text_from_pdf():
    pdf_document = fitz.open()
    page = pdf_document.new_page()
    page.insert_text((72, 72), "Python Docker AWS")
    pdf_bytes = pdf_document.tobytes()
    pdf_document.close()

    result = extract_text_from_pdf(BytesIO(pdf_bytes))

    assert "Python" in result


def test_extract_text_from_docx():
    docx_document = Document()
    docx_document.add_paragraph("Python Docker AWS")
    buffer = BytesIO()
    docx_document.save(buffer)
    buffer.seek(0)

    result = extract_text_from_docx(buffer)

    assert "Python Docker AWS" in result
