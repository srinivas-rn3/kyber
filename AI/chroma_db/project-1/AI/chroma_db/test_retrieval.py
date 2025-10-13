import chromadb
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    BEDROCK_EMBED_MODEL,
    BEDROCK_REGION
)

# Initialize Bedrock embeddings
bedrock_embeddings = BedrockEmbeddings(
    model_id=BEDROCK_EMBED_MODEL,
    region_name=BEDROCK_REGION
)

# Initialize Chroma vector store
vectorstore = Chroma(
    persist_directory=CHROMA_PATH,
    collection_name=COLLECTION_NAME,
    embedding_function=bedrock_embeddings
)

# Check what's in the database
print("=== Database Contents ===")
try:
    # Get all documents
    collection = vectorstore._collection
    all_docs = collection.get()
    
    print(f"Total documents in collection '{COLLECTION_NAME}': {len(all_docs['documents'])}")
    
    for i, (doc, metadata) in enumerate(zip(all_docs['documents'], all_docs['metadatas']), 1):
        print(f"\n{i}. {doc}")
        print(f"   Metadata: {metadata}")
        
except Exception as e:
    print(f"Error accessing collection: {e}")

print("\n=== Testing Retrieval ===")
# Test similarity search
query = "LangChain"
print(f"Searching for: '{query}'")

try:
    results = vectorstore.similarity_search(query, k=3)
    print(f"Found {len(results)} results:")
    
    for i, doc in enumerate(results, 1):
        print(f"\n{i}. {doc.page_content}")
        print(f"   Metadata: {doc.metadata}")
        
except Exception as e:
    print(f"Error during search: {e}")