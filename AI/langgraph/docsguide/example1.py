# Step 1: Define tools and model
from langchain.tools import tool
from langchain.chat_models import init_chat_model

# Initialize Bedrock model
model = init_chat_model(
    "anthropic.claude-3-haiku-20240307-v1:0",
    model_provider="bedrock",
    region_name="ap-south-1",
    temperature=0
)

# ----------------------------
# Step 2: Define tools (DOCSTRINGS REQUIRED)
# ----------------------------

@tool
def add(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers and return the result."""
    return a * b

@tool
def divide(a: int, b: int) -> float:
    """Divide the first integer by the second and return the result."""
    return a / b

tools = [add, multiply, divide]
tools_by_name = {t.name: t for t in tools}

# Bind tools to the model
model_with_tools = model.bind_tools(tools)

# ----------------------------
# Step 3: Define state
# ----------------------------

from langchain_core.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

# ----------------------------
# Step 4: Define LLM node
# ----------------------------

from langchain_core.messages import SystemMessage

def llm_call(state: MessagesState):
    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content="You are a helpful assistant that performs arithmetic using tools when needed."
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get("llm_calls", 0) + 1
    }

# ----------------------------
# Step 5: Define tool node
# ----------------------------

from langchain_core.messages import ToolMessage

def tool_node(state: MessagesState):
    results = []

    last_message = state["messages"][-1]

    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])

        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id=tool_call["id"]
            )
        )

    return {"messages": results}

# ----------------------------
# Step 6: Routing logic
# ----------------------------

from typing import Literal
from langgraph.graph import StateGraph, START, END

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    last_message = state["messages"][-1]
    return "tool_node" if last_message.tool_calls else END

# ----------------------------
# Step 7: Build the graph
# ----------------------------

agent_builder = StateGraph(MessagesState)

agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue)
agent_builder.add_edge("tool_node", "llm_call")

agent = agent_builder.compile()

# ----------------------------
# Step 8: Invoke
# ----------------------------

from langchain_core.messages import HumanMessage

initial_messages = [HumanMessage(content="mutiply 30 and 4")]
result = agent.invoke({"messages": initial_messages})

for msg in result["messages"]:
    msg.pretty_print()
