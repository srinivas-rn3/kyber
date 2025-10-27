import chromadb

#File path 
PATH = r"C:\Users\srini\OneDrive\kiro\kyber\AI\chroma_db"
# Create a local in-memory client
client = chromadb.PersistentClient(path=PATH)

# Create a collection
collection = client.create_collection(name="test_collection")

# Add some sample documents + metadata
collection.add(
    documents=[
        "Amazon Bedrock is a fully managed AI service.",
        "LangChain connects LLMs with external data sources.",
        "FAISS is used for efficient similarity search."
        ],
        ids = ["1","2","3"],
        metadatas=[
            {"source":"AWS Docs"},
            {"source":"LangChain Docs"},
            {"source":"FAISS Docs"}
        ]
)
#Query Chorma
#results = collection.query(
#    query_texts=['What is Bedrock?'],n_results=2
#)

#print(results)
print("Data Stored in disk:",PATH)

results  = collection.query(
    query_texts=['What is Bedrock?'],
    n_results=2
)
print("===== Search1: 'What is embedding:' =====")
for i ,doc in enumerate(results['documents'][0]):
    print(f"{i+1}. {doc}")
    print(f"    Source:{results['metadatas'][0][i]['source']}")
    print()