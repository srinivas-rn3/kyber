import os
from PyPDF2 import PdfReader
from config import PDF_FOLDER

def load_pdfs():
    documents = []
    if not os.path.exists(PDF_FOLDER):
        os.makedirs(PDF_FOLDER)
    for file_name in os.listdir(PDF_FOLDER):
        if file_name.endswith(".pdf"):
            path = os.path.join(PDF_FOLDER, file_name)
            reader = PdfReader(path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            documents.append({"file": file_name, "text": text})
    return documents
