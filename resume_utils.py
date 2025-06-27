# resume_utils.py (alternative using fitz)

import fitz  # PyMuPDF
import docx2txt

def extract_text_from_file(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif uploaded_file.name.endswith(".docx"):
        return docx2txt.process(uploaded_file)
    else:
        return str(uploaded_file.read(), "utf-8")

def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def get_resume_sections(text):
    lines = text.lower().split("\n")
    sections = set()
    for line in lines:
        if any(keyword in line for keyword in ["experience", "skills", "projects", "education"]):
            sections.add(line.strip())
    return sections
