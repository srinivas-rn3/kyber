from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

model = SentenceTransformer("all-mpnet-base-v2")

docs = [
    "Earth gravity is 9.8 meters per second squared.",
    "Mars gravity is 3.71 m/s2.",
    "Venus gravity is 8.87 m/s2.",
]

## Get embeddings (768-dim)
embeddings = model.encode(docs).astype('float32')

print("Embeddings shape:",embeddings.shape)
print("Embeddings vector for maer:", embeddings[1][:10])

#################33333

index = faiss.IndexFlatL2(768)
index.add(embeddings)

query = "What is the gravity of Mars?"
query_vec = model.encode([query]).astype('float32')

distance,id = index.search(query_vec, k=3)

print("Distance:", distance)
print("ID:", id)
