from langchain_aws import ChatBedrock
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool
from langchain_core.prompts import ChatPromptTemplate
from tools import search_expenses, calculate_totals
import config as Config

# Create LangChain tools
tools = [
    Tool(
        name="search_expenses",
        description="Search through expense records using natural language. Input should be a search query about expenses.",
        func=search_expenses
    ),
    Tool(
        name="calculate_totals", 
        description="Calculate mathematical expressions. Input should be a mathematical expression like '100 + 200 * 0.1'.",
        func=calculate_totals
    )
]

# Initialize the LLM
llm = ChatBedrock(model_id=Config.LLM_MODEL, region_name=Config.REGION)

# Create the prompt template for tool calling
prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a financial advisor assistant. You can help users analyze their expenses.
    
    Use the available tools to search expense records and perform calculations as needed.
    Always provide helpful, clear responses about the user's financial data."""),
    ("human", "{input}"),
    ("placeholder", "{agent_scratchpad}"),
])

def react_agent_modern(query: str):
    """
    Modern LangChain agent using function calling (if supported by the model)
    """
    try:
        # Create agent with tool calling capability
        agent = create_tool_calling_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
        
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        # Fallback to the ReAct agent if tool calling isn't supported
        print(f"Tool calling not supported, falling back to ReAct: {e}")
        from react_agent import react_agent
        return react_agent(query)