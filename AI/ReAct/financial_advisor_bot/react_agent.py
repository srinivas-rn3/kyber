from langchain_aws import ChatBedrock
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain.prompts import PromptTemplate
from tools import search_expenses, calculate_totals
import config as Config

# Create LangChain tools
langchain_tools = [
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

# Create the ReAct prompt template
react_prompt = PromptTemplate.from_template("""
You are a financial advisor assistant. Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}
""")

# Create the agent and executor
agent = create_react_agent(llm, langchain_tools, react_prompt)
agent_executor = AgentExecutor(
    agent=agent, 
    tools=langchain_tools, 
    verbose=True,
    max_iterations=5,
    handle_parsing_errors=True
)

def react_agent(query: str):
    """
    Process user query using LangChain's built-in ReAct agent
    """
    try:
        result = agent_executor.invoke({"input": query})
        return result["output"]
    except Exception as e:
        return f"I apologize, but I encountered an error: {e}. Please try rephrasing your question."  

            
        
