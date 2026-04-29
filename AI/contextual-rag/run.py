from pathlib import Path
from src.ingest import ingest
from src.hybrid_search import hybrid_search
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input.md"

print("Looking for input file at:", INPUT_FILE)

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

vectorstore, bm25_index = ingest(text)

results = hybrid_search(
    "Why does traditional RAG hallucinate?",
    vectorstore,
    bm25_index
)

for r in results[:4]:
    print("------")
    print(r)
