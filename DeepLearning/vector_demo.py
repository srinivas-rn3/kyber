# Step 2: Generate Embeddings
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

import boto3
from langchain_aws.embeddings import BedrockEmbeddings
import faiss
import numpy as np


documents = [
    "Python is a programming language that lets you work quickly and integrate systems more effectively.",
    "LangChain helps you build applications with LLMs using modular components like prompts, memory, and chains.",
    "FAISS is a library for efficient similarity search and clustering of dense vectors."
]

#create a Bedrock Embedding client
bedrock_client = boto3.client(
    service_name = "bedrock-runtime",
    region_name = "ap-south-1"
)
# Initialize Titan Embeddings
embeddings = BedrockEmbeddings(
    model_id = "amazon.titan-embed-text-v2:0",
    client=bedrock_client
)

#Convert each document into a vector
doc_vector = [embeddings.embed_query(doc) for doc in documents]

print("Generated",len(doc_vector),"embeddings")
print("Vector dimensions sample:",len(doc_vector[0]))

dimensions= len(doc_vector[0]) # Titan v2 = 1024
index = faiss.IndexFlatL2(dimensions) # L2 distance for similarity
index.add(np.array(doc_vector,dtype='float32'))

#print("Faiss index created with",index.ntotal,"vectors")

vector_np = np.array(doc_vector,dtype='float32')
dimensions = vector_np.shape[1]  # Get the number of dimensions

index = faiss.IndexFlatL2(dimensions)

index.add(vector_np)
print(f"Total vectors in index: {index.ntotal}")

query = "What is LangChain?"
query_embedding = embeddings.embed_query(query)
query_np = np.array([query_embedding],dtype='float32')

k = 2
distances,indices =  index.search(query_np, k)

print("Distances:",distances)
print("Matching indices:", indices)

def get_similar_docs(query, k=2):
    query_vector = embeddings.embed_query(query)
    query_np = np.array([query_vector], dtype='float32')
    distances , indices = index.search(query_np, k)
    results = [documents[i] for i in indices[0]]
    return results,distances[0]


results,dists =  get_similar_docs("What is FAISS?")
print("Top Documents:",results)
print("Distances:", dists)

#Documents (Text) → Embeddings (Vectors) → FAISS Index → Query → Closest Vectors → Top Documents
