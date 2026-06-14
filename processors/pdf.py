from PyPDF2 import PdfReader


def extract_pdf_text(pdf_file):

    try:

        reader = PdfReader(pdf_file)
        text = ""

        for page_num, page in enumerate(reader.pages):

            try:
                page_text = page.extract_text()

                if page_text:
                    # Add page marker to preserve order/structure
                    text += f"\n[Page {page_num + 1}]\n"
                    text += page_text + "\n"

            except Exception:
                continue

        return text.strip()

    except Exception :
        return ""