"""
Demo: Top-K retrieval WITHOUT context vs WITH context (same query)

This uses TF-IDF vectors as a stand-in for embeddings so you can run it anywhere.
It still demonstrates the effect: adding document/section context to the embedded text
pulls results into the “same section” instead of mixed domains.
"""

from dataclasses import dataclass
from typing import List, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    chunk_id: str
    section: str
    text: str


def top_k(
    query: str,
    chunks: List[Chunk],
    k: int = 5,
) -> List[Tuple[int, float, Chunk]]:
    corpus = [c.text for c in chunks]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), stop_words="english")
    doc_vecs = vectorizer.fit_transform(corpus)
    q_vec = vectorizer.transform([query])

    scores = cosine_similarity(q_vec, doc_vecs).ravel()
    ranked_idx = scores.argsort()[::-1][:k]
    return [(i, float(scores[i]), chunks[i]) for i in ranked_idx]


def print_results(title: str, results: List[Tuple[int, float, Chunk]]):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)
    for rank, (i, score, c) in enumerate(results, start=1):
        snippet = (c.text[:120] + "...") if len(c.text) > 120 else c.text
        print(f"{rank:02d}. score={score:.4f} | section={c.section:22} | id={c.chunk_id} | {snippet}")


# -------------------------------------------------------------------------
# Data: same "chunk text" appears across mixed domains.
# -------------------------------------------------------------------------
raw_chunks = [
    Chunk("EVAL-1", "Experimental results", "The model achieved 82% accuracy on the benchmark."),
    Chunk("EVAL-2", "Experimental results", "We compared retrieval accuracy across BM25, dense retrieval, and hybrid search."),
    Chunk("EVAL-3", "Experimental results", "Accuracy improved when we used context-aware representations for retrieval."),
    Chunk("IMG-1", "Computer vision", "The image classification model achieved 82% accuracy on the benchmark."),
    Chunk("MKT-1", "Marketing analytics", "Campaign accuracy metrics improved by 8% after audience segmentation."),
    Chunk("SUR-1", "User research", "Survey results show accuracy of responses improved with better onboarding."),
    Chunk("OPS-1", "Operations", "Accuracy in inventory forecasting improved after fixing data drift."),
]

query = "What accuracy did the retrieval model achieve?"
K = 5

# -------------------------------------------------------------------------
# WITHOUT context: embed only raw chunk text
# -------------------------------------------------------------------------
results_without = top_k(query=query, chunks=raw_chunks, k=K)
print_results("Top-K results WITHOUT context → mixed domains", results_without)

# -------------------------------------------------------------------------
# WITH context: enrich each chunk *before embedding*
# (simulate Anthropic-style doc/section/intent context)
# -------------------------------------------------------------------------
DOC_SUMMARY = "Document summary: Evaluation of LLM retrieval systems and benchmark results."
SECTION_CONTEXT = {
    "Experimental results": "Section summary: Retrieval experiments and metrics (accuracy/recall).",
    "Computer vision": "Section summary: Image classification evaluation metrics.",
    "Marketing analytics": "Section summary: Marketing performance and attribution metrics.",
    "User research": "Section summary: Surveys, qualitative feedback, and UX metrics.",
    "Operations": "Section summary: Forecasting, supply chain, and operational KPIs.",
}
INTENT_CONTEXT = {
    "Experimental results": "Paragraph intent: Report retrieval model performance.",
    "Computer vision": "Paragraph intent: Report vision model performance.",
    "Marketing analytics": "Paragraph intent: Report marketing metric changes.",
    "User research": "Paragraph intent: Report survey outcomes.",
    "Operations": "Paragraph intent: Report operational forecasting performance.",
}

contextual_chunks = []
for c in raw_chunks:
    enriched = "\n".join(
        [
            DOC_SUMMARY,
            SECTION_CONTEXT.get(c.section, f"Section summary: {c.section}."),
            INTENT_CONTEXT.get(c.section, "Paragraph intent: Provide supporting detail."),
            f"Text: {c.text}",
        ]
    )
    contextual_chunks.append(Chunk(chunk_id=c.chunk_id, section=c.section, text=enriched))

results_with = top_k(query=query, chunks=contextual_chunks, k=K)
print_results("Top-K results WITH context → same section", results_with)
