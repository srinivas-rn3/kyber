from langchain_chroma import Chroma
from ingest.embedder import get_titan_embeddings

def get_retriever():
    embeddings = get_titan_embeddings()

    vectordb = Chroma(
        collection_name="docs",
        persist_directory="vector_store",
        embedding_function=embeddings
    )

    # retriever with .invoke() support
    return vectordb.as_retriever(search_kwargs={"k": 3})
