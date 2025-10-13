import chromadb
import os
import sqlite3
import pandas as pd

# Connect to the ChromaDB SQLite file
conn = sqlite3.connect(r'C:\Users\srini\OneDrive\kiro\kyber\AI\chroma_db\chroma.sqlite3')

# See all tables
table_query = "SELECT  name FROM sqlite_master WHERE type='table';"
tables = pd.read_sql_query(table_query, conn)
print("Tables in chromaDB SQLLite:")
print(tables)

# See what's in the collections table
collections_data =pd.read_sql_query("SELECT * FROM collections;", conn)
print("\n Collections:")
print(collections_data)

# See embeddings metadata
embeedings_data = pd.read_sql_query("SELECT * FROM embeddings;", conn)
print("\n Embeddings Metadata:")
print(embeedings_data)

conn.close()