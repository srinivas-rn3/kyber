from langgraph.graph import StateGraph,END
from typing import TypedDict

#Step 1: Define the State
class State(TypedDict):
    message: str
    intent: str

#Step 2: Create Nodes
def greet(state: State):
    print("Hi! What can I help you with today?")
    state['message'] = input(">>")
    return state

def classify(state:State):
    msg = state['message'].lower()
    if "weather" in msg:
        state['intent'] = "weather"
    elif "alarm" in msg:
        state['intent'] = "alarm"
    elif "bye" in msg:
        state['intent'] = "exit"
    else:
        state['intent'] = "unknown"
    return state

def weather_node(state:State):
    print("Weather today is sunny and pleasent.")
    return state

def alarm_node(state:State):
    print("Alarm for tomorrow morning is set at 6:00 AM.")
    return state

def fallback(state:State):
    print("Sorry, I don't understand.")
    return state

#Step 3: Decision Function
def route_intent(state:State):
    intent = state['intent']
    if intent == "weather":
        return "weather"
    elif intent == "alarm":
        return "alarm"
    elif intent == "exit":
        return "exit"
    else:
        return "unknown"

#Step 4: Build the Graph

workflow = StateGraph(State)

#ADD NODES
workflow.add_node("greet",greet)
workflow.add_node("classify", classify)
workflow.add_node("weather", weather_node)
workflow.add_node("alarm", alarm_node)
workflow.add_node("fallback", fallback)

#ENTRY POINT
workflow.set_entry_point("greet")

#ADD LINEAR EDGE FIRST
workflow.add_edge("greet", "classify")


# Add conditional edges based on intent
workflow.add_conditional_edges(
    "classify",
    route_intent,
    {
        "weather": "weather",
        "alarm": "alarm",
        "unknown": "fallback",
        "exit": END
    }
)
#Step 5: Compile and Run
app = workflow.compile()
app.invoke({})