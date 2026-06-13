from pptx import Presentation

def extract_ppt_text(ppt_file):

    prs = Presentation(ppt_file)

    text = ""

    for slide in prs.slides:

        for shape in slide.shapes:

            if hasattr(shape, "text"):
                text += shape.text + "\n"

    return text