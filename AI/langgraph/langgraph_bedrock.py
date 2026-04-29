from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from typing import TypedDict

#Step 1. Import Libraries and Setup LLM

# ---------------------------------------------
# 🔧 Initialize Bedrock model
# ---------------------------------------------
region = "ap-south-1"
model_id = "anthropic.claude-3-haiku-20240307-v1:0"

llm = ChatBedrock(
    model_id = model_id,
    region_name = region,
)

#Step 2. Define the State

class State(TypedDict):
    message: str
    intent: str

#Step 3. Define Nodes

def greet(state:State):
    print("👋 Hi! What can I help you with today?")
    state['message'] = input(">>").strip().lower()
    return state

#LLM Classifier Node
def classify_with_llm(state:State):
    usr_msg = state['message']

    prompt = f"""
    You are an intent classifier. 
    Based on the user's message, return one of the following intents:
    - weather
    - alarm
    - exit

    Only respond with the intent word.

    User: {usr_msg}
    """

    response = llm.invoke(prompt)
    intent = response.content.strip().lower()

    #Validate response
    if intent not in ["weather", "alarm", "exit"]:
        intent = "unknown"
    print(f"🤖 Detected intent: {intent}")
    state["intent"] = intent
    return state

#Action Nodes
def weather_node(state: State):
    print("🌤️ The weather today is warm and pleasant.")
    return state

def alarm_node(state: State):
    print("🔔 Setting an alarm for 7:00 AM.")
    return state

def fallback_node(state: State):
    print("🤖 I'm sorry, I didn't understand that.")
    return state

#Step 4. Decision Function
def route_intent(state: State):
    intent = state['intent']
    if intent == "weather":
        return "weather"
    elif intent == "alarm":
        return "alarm"
    elif intent == "exit":
        return "exit"
    else:
        return "unknown"

#Step 5. Build the Graph
workflow = StateGraph(State)

workflow.add_node("greet", greet)
workflow.add_node("classify", classify_with_llm)
workflow.add_node("weather", weather_node)
workflow.add_node("alarm", alarm_node)
workflow.add_node("fallback", fallback_node)

workflow.set_entry_point("greet")
workflow.add_edge("greet", "classify")

workflow.add_conditional_edges(
    "classify",
    route_intent,
    {
        "weather": "weather",
        "alarm": "alarm",
        "exit": END,
        "unknown": "fallback"
    }
)

#Step 6. Run the Graph
app = workflow.compile()
app.invoke({})

