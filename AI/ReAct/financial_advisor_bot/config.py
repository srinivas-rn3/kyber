# ----------- File Locations -----------
KB_FILE = r"C:\Users\srini\OneDrive\kiro\kyber\AI\ReAct\financial_advisor_bot\KB\expenses.csv"
FAISS_INDEX = r"C:\Users\srini\OneDrive\kiro\kyber\AI\ReAct\financial_advisor_bot\embeeding_vector\faiss_index"
VECTOR_DB = FAISS_INDEX  # Alias for consistency

# ----------- Model IDs (AWS Bedrock) -----------
EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"
LLM_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
#-------------- Region -----------
REGION = "ap-south-1"
# ----------- Other Parameters -----------
CHUNK_SIZE = 300
CHUNK_OVERLAP = 50
TOP_K = 3   # number of docs retrieved from KB
