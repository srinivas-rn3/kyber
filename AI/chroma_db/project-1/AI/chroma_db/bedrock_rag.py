import chromadb
from langchain_aws import BedrockEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA
from langchain_aws import ChatBedrock
from config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    BEDROCK_EMBED_MODEL,
    BEDROCK_LLM_MODEL,
    BEDROCK_REGION
)

# -------------------------------
# Initialize persistent Chroma client
# -------------------------------
client = chromadb.PersistentClient(path=CHROMA_PATH)

# -------------------------------
# Initialize Bedrock embeddings
# region is explicitly passed here
# -------------------------------
bedrock_embeddings = BedrockEmbeddings(
    model_id=BEDROCK_EMBED_MODEL,
    region_name=BEDROCK_REGION
)

# -------------------------------
# Initialize Chroma vector store
# -------------------------------
vectorstore = Chroma(
    client=client,
    collection_name=COLLECTION_NAME,
    embedding_function=bedrock_embeddings
)

# -------------------------------
# Initialize Bedrock LLM
# region is explicitly passed here
# -------------------------------
llm = ChatBedrock(
    model_id=BEDROCK_LLM_MODEL,
    region_name=BEDROCK_REGION
)

# -------------------------------
# Setup RetrievalQA chain
# -------------------------------
retriever = vectorstore.as_retriever()

from langchain.prompts import PromptTemplate

# Create a custom prompt that instructs the LLM to stick to the retrieved content
prompt_template = """Use only the following context to answer the question. Do not add any information beyond what is provided in the context.

Context: {context}

Question: {question}

Answer based only on the context above:"""

PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    chain_type_kwargs={"prompt": PROMPT}
)

# -------------------------------
# Run query
# -------------------------------
query = "Explain LangChain in simple terms"
print("Query:", query)
print("\n" + "="*50)

# Show what documents were retrieved from Chroma
print("Documents retrieved from Chroma:")
retrieved_docs = retriever.invoke(query)
for i, doc in enumerate(retrieved_docs, 1):
    print(f"{i}. {doc.page_content}")
    print(f"   Source: {doc.metadata.get('source', 'Unknown')}")

print("\n" + "="*50)

# Get the final answer
result = qa_chain.invoke({"query": query})
print("Final Answer:")
print(result["result"])
