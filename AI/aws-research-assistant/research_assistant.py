# research_assistant.py
import os
import boto3
from langchain_community.chat_models import BedrockChat
from langchain.prompts import PromptTemplate

from config import *
from memory import SimpleMemory
from vector_store import SimpleVectorStore

class SimpleResearchAssistant:
    def __init__(self, session_id):
        self.session_id = session_id
        
        # AWS clients (uses your CLI credentials automatically)
        self.bedrock_runtime = boto3.client('bedrock-runtime', region_name=AWS_REGION)
        
        # Initialize components
        self.memory = SimpleMemory(session_id)
        self.vector_store = SimpleVectorStore()
        self.llm = BedrockChat(
            model_id=CHAT_MODEL,
            client=self.bedrock_runtime,
            model_kwargs={
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS
            }
        )
        
        # Try to load existing vector store
        if self.vector_store.load_existing_store():
            print("✓ Loaded existing vector store")
        else:
            print("! No existing vector store found")
        
        print(f"Research Assistant ready! Session: {session_id}")
    
    def load_documents(self):
        """Load all documents from the documents folder"""
        if not os.path.exists(DOCUMENT_FOLDER):
            print(f"Creating '{DOCUMENT_FOLDER}' folder...")
            os.makedirs(DOCUMENT_FOLDER)
            print(f"Please add your PDF files to the '{DOCUMENT_FOLDER}' folder and run again.")
            return
        
        document_paths = [
            os.path.join(DOCUMENT_FOLDER, f) 
            for f in os.listdir(DOCUMENT_FOLDER) 
            if f.endswith('.pdf')
        ]
        
        if not document_paths:
            print(f"No PDF files found in '{DOCUMENT_FOLDER}' folder!")
            return
        
        print(f"Loading {len(document_paths)} documents...")
        # FIXED: Changed from load_document to load_documents
        self.vector_store.load_documents(document_paths)
        print("✓ Documents loaded successfully!")
    
    def ask(self, question):
        """Ask a question and get an answer"""
        print(f"Q: {question}")
        
        # Search for relevant documents
        relevant_docs = self.vector_store.search(question)
        
        if not relevant_docs:
            return {
                "answer": "I couldn't find relevant information. Please make sure documents are loaded.",
                "sources": []
            }
        
        # Get conversation history
        history = self.memory.get_history(limit=5)
        history_text = ""
        if history:
            history_text = "\nPrevious conversation:\n"
            for item in history:
                history_text += f"Human: {item['question']}\nAssistant: {item['answer']}\n\n"
        
        # Build context from documents
        context = "\n\n".join([
            f"From {doc.metadata['source_file']}:\n{doc.page_content}"
            for doc in relevant_docs
        ])
        
        # Create prompt
        prompt = f"""You are a helpful research assistant. Use the context below to answer the question.

{history_text}

Relevant information:
{context}

Question: {question}

Provide a helpful answer based on the information above. If you're not sure, say so.

Answer:"""
        
        # Get answer
        response = self.llm.invoke(prompt)
        answer = response.content
        
        # Get sources
        sources = list(set([doc.metadata['source_file'] for doc in relevant_docs]))
        
        # Save to memory
        self.memory.save_conversation(question, answer, sources)
        
        return {
            "answer": answer,
            "sources": sources,
            "documents_used": len(relevant_docs)
        }
    
    def get_session_info(self):
        """Get basic session information"""
        history = self.memory.get_history()
        return {
            "session_id": self.session_id,
            "questions_asked": len(history),
            "model": CHAT_MODEL
        }