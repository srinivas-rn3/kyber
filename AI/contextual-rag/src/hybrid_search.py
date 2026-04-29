# src/hybrid_search.py
def hybrid_search(
    query: str,
    vectorstore,
    bm25_index,
    k_embed: int = 3,
    k_bm25: int = 3
):
    embed_results = vectorstore.similarity_search(query, k=k_embed)
    bm25_results = bm25_index.search(query, k=k_bm25)

    embed_texts = [r.page_content for r in embed_results]

    # Deduplicate + prioritize embedding results
    merged = []
    seen = set()

    for text in embed_texts:
        merged.append(text)
        seen.add(text)

    for text in bm25_results:
        if text not in seen:
            merged.append(text)

    return merged

