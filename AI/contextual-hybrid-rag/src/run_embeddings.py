import os
import warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  # Suppress TensorFlow INFO and WARNING messages
warnings.filterwarnings("ignore", category=DeprecationWarning)

from ingest.chunker import chunk_sections
from ingest.pipeline import contextualize
from llm.bedrock_llm import BedrockLLM
from embed import Embedder
from pathlib import Path
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'  # Suppress INFO messages


doc_title = "Company Leave Policy"
BASE_DIR = Path(__file__).resolve().parent.parent
text = open(BASE_DIR / "data" / "leave_policy.md").read()

# Step 1: chunk
chunks = chunk_sections(text)

# Step 2: contextualize (already working)
llm = BedrockLLM()
contextual_chunks = contextualize(doc_title, chunks, llm)

# Step 3: embed both versions
embedder = Embedder()

raw_texts = [c["raw_text"] for c in contextual_chunks]
contextual_texts = [c["contextual_text"] for c in contextual_chunks]

raw_embeddings = embedder.embed(raw_texts)
context_embeddings = embedder.embed(contextual_texts)

print("Raw embedding shape:", raw_embeddings.shape)
print("Context embedding shape:", context_embeddings.shape)