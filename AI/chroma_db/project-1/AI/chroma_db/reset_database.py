import chromadb
import shutil
import os
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    BEDROCK_EMBED_MODEL,
    BEDROCK_REGION
)

# Remove existing database
if os.path.exists(CHROMA_PATH):
    shutil.rmtree(CHROMA_PATH)
    print(f"Removed existing database at: {CHROMA_PATH}")

# Initialize Bedrock embeddings
bedrock_embeddings = BedrockEmbeddings(
    model_id=BEDROCK_EMBED_MODEL,
    region_name=BEDROCK_REGION
)

# Create new database with correct embeddings
vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    collection_name=COLLECTION_NAME,
    embedding_function=bedrock_embeddings
)

# Add sample documents
documents = [
    "Amazon Bedrock is a fully managed AI service that provides access to foundation models from leading AI companies through a single API.",
    "LangChain is a framework for developing applications powered by language models. It connects LLMs with external data sources and tools.",
    "FAISS (Facebook AI Similarity Search) is a library for efficient similarity search and clustering of dense vectors.",
    "Vector databases store and retrieve high-dimensional vectors efficiently, enabling semantic search and similarity matching.",
    "RAG (Retrieval-Augmented Generation) combines information retrieval with text generation to provide more accurate and contextual responses."
]

metadatas = [
    {'source': 'AWS Docs', 'topic': 'Bedrock'},
    {'source': 'LangChain Docs', 'topic': 'Framework'},
    {'source': 'FAISS Docs', 'topic': 'Search'},
    {'source': 'Vector DB Guide', 'topic': 'Storage'},
    {'source': 'RAG Guide', 'topic': 'Architecture'}
]

vectorstore.add_texts(
    texts=documents,
    metadatas=metadatas
)

print(f"Database recreated successfully at: {CHROMA_PATH}")
print(f"Added {len(documents)} documents to collection: {COLLECTION_NAME}")