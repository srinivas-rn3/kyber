from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings
import config as Config
import os

# Global variable to store the database instance
_db = None

def _get_db():
    """Lazy loading of the vector database"""
    global _db
    if _db is None:
        embeddings = BedrockEmbeddings(model_id=Config.EMBEDDING_MODEL, region_name=Config.REGION)
        _db = FAISS.load_local(Config.VECTOR_DB, embeddings=embeddings, allow_dangerous_deserialization=True)
    return _db

def search_expenses(query: str) -> str:
    try:
        db = _get_db()
        docs = db.similarity_search(query, k=Config.TOP_K)
        return "\n".join([d.page_content for d in docs])
    except Exception as e:
        return f"Error searching expenses: {e}"

def calculate_totals(expr: str) -> str:
    try:
        return str(eval(expr))
    except Exception as e:
        return f"Error: {e}"


