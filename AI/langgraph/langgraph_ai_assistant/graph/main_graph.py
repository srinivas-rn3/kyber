from langgraph.graph import StateGraph, END
from typing import TypedDict

from nodes.greeting_node import greet
from nodes.classify_node import classify_with_llm
from nodes.weather_node import weather_node
from nodes.alarm_node import alarm_node
from nodes.fallback_node import fallback_node
from memory.memory_handler import update_memory

# ----- Define State -----
class State(TypedDict):
    message: str
    intent: str
    history: list

# ----- Decision Function -----
def route_intent(state: State):
    intent = state["intent"]
    if intent == "weather":
        return "weather"
    elif intent == "alarm":
        return "alarm"
    elif intent == "exit":
        return "exit"
    else:
        return "unknown"

# ----- Build Graph -----
def build_graph():
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
            "unknown": "fallback",
            "exit": END
        }
    )

    return workflow.compile()
