from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain_community.vectorstores import FAISS
import config

# 1. Load Vector DB
embeddings = BedrockEmbeddings(
    model_id=config.EMBEDDING_MODEL,
    region_name=config.REGION
)
db = FAISS.load_local(config.FAISS_INDEX, embeddings, allow_dangerous_deserialization=True)

# 2. LLM
llm = ChatBedrock(
    model_id=config.LLM_MODEL,
    region_name=config.REGION
)

# 3. Simple RAG function
def answer_question(query: str) -> str:
    # Search KB
    docs = db.similarity_search(query, k=config.TOP_K)
    context = "\n".join([d.page_content for d in docs])
    
    # Create prompt
    prompt = f"""
    Based on the following knowledge base information, answer the user's question.
    
    Knowledge Base Context:
    {context}
    
    User Question: {query}
    
    Answer:"""
    
    # Get response from LLM
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        return f"Error getting LLM response: {e}\n\nDirect KB info:\n{context}"

# 4. Run Query
if __name__ == "__main__":
    query = "How do I reset my OpenText Password?"
    result = answer_question(query)
    print(f"\nQuestion: {query}")
    print(f"Answer: {result}")