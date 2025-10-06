# config.py
"""
Simple configuration for AWS Research Assistant
Uses your existing AWS CLI credentials automatically
"""

# AWS Configuration (uses your existing AWS CLI credentials)
AWS_REGION = "ap-south-1"  # Change if needed

# Model Configuration
CHAT_MODEL = "anthropic.claude-3-haiku-20240307-v1:0"
EMBEDDING_MODEL = "amazon.titan-embed-text-v2:0"

# File Paths
DOCUMENT_FOLDER = r"C:\Users\srini\OneDrive\kiro\kyber\AI\aws-research-assistant\documents"
VECTOR_STORE_PATH = r"C:\Users\srini\OneDrive\kiro\kyber\AI\aws-research-assistant\vector-store"

# Memory Configuration
DYNAMODB_TABLE = "research-assistant-memory"

# Search Configuration
SIMILARITY_TOP_K = 4
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Model Parameters
TEMPERATURE = 0.1
MAX_TOKENS = 2000

# UI Settings
SHOW_SOURCES = True
SHOW_CONFIDENCE = True