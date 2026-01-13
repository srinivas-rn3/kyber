def search(vectorstore, query, k=3):
    return vectorstore.similarity_search(query, k=k)
