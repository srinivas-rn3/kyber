import chromadb
from config import CHROMA_PATH,COLLECTION_NAME

client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.create_collection(name=COLLECTION_NAME)


collection.add(
    documents=[
        "Amazon Bedrock is a fully managed AI service.",
        "LangChain connects LLMs with external data sources.",
        "FAISS is used for efficient similarity search."
    ],
    ids = ['1','2','3'],
    metadatas = [
        {'source':'AWS Docs'},
        {'source':'Langchain Docs'},
        {'source':'FIASS Docs'}
    ]
     
)
print("Collection created and stored at:",CHROMA_PATH)
