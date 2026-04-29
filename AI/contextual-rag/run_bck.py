from pathlib import Path
from src.ingest import ingest
import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "data" / "input.md"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

vectorstore = ingest(text)

results = vectorstore.similarity_search(
    "Why does traditional RAG fail?",
    k=2
)

for r in results:
    print("------")
    print(r.page_content)
