import faiss
import numpy as np

vectors = np.array([
    [0.10, 0.80],    # Earth
    [0.90, 1.00],    # Mars
    [0.20, 0.70],    # Venus
]).astype('float32')

index  = faiss.IndexFlatL2(2)
index.add(vectors)

query = np.array([[0.88, 0.95]]).astype('float32')
distance,ids = index.search(query,k=3)

print("Distance : ",distance)
print("IDs :", ids)