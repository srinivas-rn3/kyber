# vector_store.py
import os
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import BedrockEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import boto3
from config import *

class SimpleVectorStore:
    def __init__(self):
        self.embeddings = BedrockEmbeddings(
            client=boto3.client('bedrock-runtime', region_name=AWS_REGION),
            model_id=EMBEDDING_MODEL
        )
        self.vector_store = None
    
    def load_documents(self, document_paths):
        all_docs = []
        
        for doc_path in document_paths:
            if doc_path.endswith('.pdf'):
                loader = PyPDFLoader(doc_path)
                documents = loader.load()
                
                for doc in documents:
                    doc.metadata['source_file'] = os.path.basename(doc_path)
                
                all_docs.extend(documents)
                print(f"Loaded {len(documents)} chunks from {os.path.basename(doc_path)}")
        
        if not all_docs:
            print("No documents loaded!")
            return
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        splits = text_splitter.split_documents(all_docs)
        
        self.vector_store = FAISS.from_documents(splits, self.embeddings)
        
        os.makedirs(VECTOR_STORE_PATH, exist_ok=True)
        self.vector_store.save_local(VECTOR_STORE_PATH)
        print(f"Saved vector store with {len(splits)} chunks")
    
    def load_existing_store(self):
        try:
            self.vector_store = FAISS.load_local(
                VECTOR_STORE_PATH, 
                self.embeddings,
                allow_dangerous_deserialization=True
            )
            return True
        except:
            return False
    
    def search(self, query):
        if not self.vector_store:
            return []
        return self.vector_store.similarity_search(query, k=SIMILARITY_TOP_K)