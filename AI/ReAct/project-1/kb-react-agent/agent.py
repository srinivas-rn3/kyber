from langchain_aws import ChatBedrock, BedrockEmbeddings
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_community.vectorstores import FAISS
import config

# 1. Load Vector DB
embeddings = BedrockEmbeddings(
    model_id=config.EMBEDDING_MODEL,
    region_name=config.REGION
)
db = FAISS.load_local(config.FAISS_INDEX, embeddings, allow_dangerous_deserialization=True)


## 2. KB Search Tool
def search_kb(query: str) -> str:
    docs = db.similarity_search(query, k=config.TOP_K)
    return "\n".join([d.page_content for d in docs])

tools = [Tool(
    name="search_kb",
    func=search_kb,
    description="Search KB Articles for relevant information"
)]

# 3. LLM (Claude Haiku)
llm = ChatBedrock(
    model_id=config.LLM_MODEL,
    region_name=config.REGION
)

# 4. ReAct Agent
agent = initialize_agent(
    tools, 
    llm, 
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
    verbose=True, 
    max_iterations=5,
    return_intermediate_steps=True
)

# Run Query
query = "How do I reset my OpenText Password?"
try:
    result = agent.invoke({"input": query})
    print("\nFinal Answer:", result["output"])
except Exception as e:
    print(f"Error: {e}")
    # Fallback: direct search
    print("\nFallback - Direct KB Search:")
    kb_result = search_kb(query)
    print(kb_result)