import json
import faiss
import numpy as np
from config import INDEX_PATH, DOCS_PATH,EMBEDDING_MODEL,REGION
from langchain_aws import BedrockEmbeddings

class VectorStore:
    def __init__(self):
        self.embeddings_model = BedrockEmbeddings(model_id=EMBEDDING_MODEL, region_name=REGION)
        self.index = None
        self.docs = []

    def create_index(self, docs):
        self.docs = docs
        texts = [d["text"] for d in docs]
        # Use embed_documents instead of embed_document
        vectors = np.array(self.embeddings_model.embed_documents(texts), dtype="float32")
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)


    def save_index(self):
        if self.index is not None:
            faiss.write_index(self.index, INDEX_PATH)
            with open(DOCS_PATH, "w", encoding="utf-8") as f:
                json.dump(self.docs, f)
            print(f"[green]Saved FAISS index to {INDEX_PATH}[/green]")
        else:
            print("[red]No index to save[/red]")

    def load_index(self):
        self.index = faiss.read_index(INDEX_PATH)
        with open(DOCS_PATH, "r", encoding="utf-8") as f:
            self.docs = json.load(f)

    def search(self, query_vec, top_k=3):
        D, I = self.index.search(query_vec.reshape(1, -1), top_k)
        return [self.docs[i] for i in I[0]]
