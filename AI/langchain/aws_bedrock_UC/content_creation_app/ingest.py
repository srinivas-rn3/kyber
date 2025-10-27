from pdf_loader import load_pdfs
from vector_store import VectorStore
import numpy as np

# Load PDFs
docs = load_pdfs()
if not docs:
    print("No PDFs found in data/pdfs/")
    exit()

# Create FAISS index
store = VectorStore()
store.create_index(docs)

# Save FAISS index
store.save_index()
