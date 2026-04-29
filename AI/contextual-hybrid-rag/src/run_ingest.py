from ingest.chunker import chunk_sections
from ingest.pipeline import contextualize
from llm.bedrock_llm import BedrockLLM
from pathlib import Path
import os

# Fix OpenMP duplicate lib warning (safe)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

# -------- CONFIG --------
doc_title = "Company Leave Policy"

BASE_DIR = Path(__file__).resolve().parent.parent
INPUT_FILE = BASE_DIR / "data" / "leave_policy.md"

print("Looking for input file at:", INPUT_FILE)

# -------- LOAD DOCUMENT --------
with open(INPUT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# -------- CHUNK --------
chunks = chunk_sections(text)
print(f"\nCreated {len(chunks)} chunks")

# -------- LLM --------
llm = BedrockLLM()

# -------- CONTEXTUALIZE --------
contextual_chunks = contextualize(doc_title, chunks, llm)

# -------- PRINT RESULT --------
for c in contextual_chunks:
    print("\n-------------------------------------------")
    print(c["contextual_text"])
