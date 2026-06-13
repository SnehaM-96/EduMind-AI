from docx import Document

def extract_docx_text(docx_file):

    doc = Document(docx_file)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text