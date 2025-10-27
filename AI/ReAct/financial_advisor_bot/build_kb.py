from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
from load_data import load_expenses
import config as Config

def build_kb():
    import os
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(Config.VECTOR_DB), exist_ok=True)
    
    # Load and process documents
    docs = load_expenses(Config.KB_FILE)
    if not docs:
        raise ValueError("No documents loaded from the KB file")
    
    # Create embeddings and build vector store
    embeddings = BedrockEmbeddings(model_id=Config.EMBEDDING_MODEL,
                                   region_name=Config.REGION)
    db = FAISS.from_documents(docs, embeddings)
    db.save_local(Config.VECTOR_DB)
    return db

