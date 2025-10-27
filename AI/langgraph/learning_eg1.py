from langgraph.graph import StateGraph, MessagesState, END
from langchain_aws import ChatBedrock
from langchain_core.messages import HumanMessage

region = "ap-south-1"
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

llm = ChatBedrock(model_id=model_id, region_name=region)

# --- Define the node ---
def greeter(state: MessagesState):
    """Takes user input and replies politely"""
    messages = state['messages']
    # Get the last human message
    user_input = messages[-1].content if messages else "Hello"
    
    # Create a prompt for the LLM
    prompt = f"User said: {user_input}. Reply in one short sentence."
    response = llm.invoke([HumanMessage(content=prompt)])
    
    # Add the response to messages
    return {"messages": [response]}

#----- Create the graph -----
graph = StateGraph(MessagesState)
graph.add_node("greeter", greeter)
graph.set_entry_point("greeter")
graph.set_finish_point("greeter")

app = graph.compile()

# Test the graph
result = app.invoke({"messages": [HumanMessage(content="Hello LangGraph!!")]})
print("Final result:")
for message in result["messages"]:
    print(f"{message.__class__.__name__}: {message.content}")

