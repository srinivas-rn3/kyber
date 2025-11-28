# RAG Vector Pipeline (Chroma + AWS Titan Embeddings)

### Commands:

1. Add PDFs to /docs/
2. Run ingestion:
   python ingest/ingest.py

3. Query:
   python query/query.py

The vector database is stored in /vector_store/ and is persistent.

Titan Embeddings are used for chunk embedding.
