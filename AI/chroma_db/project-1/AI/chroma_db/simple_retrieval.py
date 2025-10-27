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

# Simple retrieval without generation
query = "Explain LangChain in simple terms"
print("Query:", query)
print("\nDirect answer from database:")

# Get the most relevant document
results = vectorstore.similarity_search(query, k=1)
if results:
    print(results[0].page_content)
else:
    print("No relevant information found in database.")