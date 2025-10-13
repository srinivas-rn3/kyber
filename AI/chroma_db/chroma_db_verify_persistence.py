import chromadb

PATH = r"C:\Users\srini\OneDrive\kiro\kyber\AI\chroma_db"
client = chromadb.PersistentClient(path=PATH)
# Load your existing collection
collection =  client.get_collection(name="test_collection")
"""
results = collection.query(
    query_texts =['Explaine Langchain'],
    n_results=2 
)
for i , doc in enumerate(results['documents'][0]):
    print(f"{i+1}.doc")
    print(f"      Source:{results['metadatas'][0][i]['source']}")
"""
questions = [
    "What is LangChain used for?",
    "What library is used for similarity search?",
    "Tell me about Bedrock"
]
for q in questions:
    results = collection.query(query_texts=[q],n_results=2)
    print(f"Query:{q}")
    for i,doc in enumerate(results['documents'][0]):
        print(f"{i+1}. {doc}")
        print(f" Source:{results['metadatas'][0][i]['source']}")
    print()


