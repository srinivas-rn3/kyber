# rag_doc_chat.py
import boto3
import numpy as np
from pdf_loader import load_pdfs
from vector_store import VectorStore
from config import REGION, MODEL_ID,EMBEDDING_MODEL

def chat():
    # Step 1: Load PDFs
    docs = load_pdfs()

    # Step 2: Create FAISS index
    store = VectorStore()
    store.create_index(docs)
    embeddings_model = EMBEDDING_MODEL

    # Step 3: Chat loop
    bedrock = boto3.client("bedrock-runtime", region_name=REGION)

    print("Chat with your documents! Type 'exit' to quit.\n")
    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        # Step 3a: Embed the query
        query_vec = np.array(embeddings_model.embed_documents([query]), dtype="float32")[0]
        # Retrieve context
        results = store.search(query_vec, k=2)
        context = "\n\n".join([r["text"][:500] for r in results])

        # Call Claude Haiku
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body={
                "messages": [
                    {"role": "user", "content": f"Answer using context:\n{context}\n\nQ: {query}"}
                ],
                "max_tokens": 300
            }
        )
        print("Bot:", response["output"]["text"])

if __name__ == "__main__":
    chat()
