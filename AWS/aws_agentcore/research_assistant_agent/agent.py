from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_aws import ChatBedrock
from langchain_community.tools import DuckDuckGoSearchRun

# Define the state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# Initialize the search tool
search_tool = DuckDuckGoSearchRun()
tools = [search_tool]

# Initialize Bedrock LLM for us-east-1
llm = ChatBedrock(model_id="anthropic.claude-3-haiku-20240307-v1:0", region="us-east-1")
llm_with_tools = llm.bind_tools(tools)

## Define the chatbot node
def chatbot(state: State):
    return {"messages": llm_with_tools.invoke(state["messages"])}

# Build the graph
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)
graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)

graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")

## Compile the graph

graph = graph_builder.compile()