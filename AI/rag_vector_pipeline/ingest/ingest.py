from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from ingest.chunker import chunk_documents
from ingest.embedder import get_titan_embeddings
from utils.file_utils import filter_new_files

PERSIST_DIR = "vector_store"
DOCS_DIR = "docs"

def get_new_docs():
    loader = DirectoryLoader(DOCS_DIR, glob="**/*.pdf")
    docs = loader.load()

    files = [doc.metadata["source"] for doc in docs]
    new_files = filter_new_files(files)
    return [doc for doc in docs if doc.metadata["source"] in new_files]

def ingest():
    new_docs = get_new_docs()

    if not new_docs:
        print("No new documents to ingest.")
        return

    print(f"Found {len(new_docs)} new documents...")

    chunks = chunk_documents(new_docs)
    embeddings = get_titan_embeddings()

    vectordb = Chroma(
        collection_name="docs",
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings
    )

    vectordb.add_documents(chunks)

    print(f"✨ Successfully added {len(chunks)} chunks to vector DB.")

if __name__ == "__main__":
    ingest()
