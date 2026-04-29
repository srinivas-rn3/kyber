# src/bm25_index.py
from rank_bm25 import BM25Okapi

class BM25Index:
    def __init__(self, texts: list[str]):
        self.texts = texts
        tokenized = [t.lower().split() for t in texts]
        self.bm25 = BM25Okapi(tokenized)

    def search(self, query: str, k: int = 3):
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)

        ranked = sorted(
            zip(scores, self.texts),
            key=lambda x: x[0],
            reverse=True
        )

        return [text for score, text in ranked[:k]]
