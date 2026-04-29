from langgraph.graph import StateGraph, END
from typing import TypedDict
from nodes.classify_node import classify_with_llM
from nodes.flight_check_node import flight_check_node
from nodes.book_flight_node import book_flight_node
from nodes.cancel_flight_node import cancel_flight_node
from nodes.response_node import response_node

class State(TypedDict):
    message: str
    intent: str
    destination: str
    date: str
    time: str
    airlines: str
    flight_result: str
    history: list

def route_intent(state: State):
    intent = state["intent"]
    if intent == "check_flight":
        return "flight_check"
    elif  intent == "book_flight":
        return "book_flight"
    elif intent == "cancel_flight":
        return "cancel_flight"
    elif intent == "exit":
        return "exit"
    else:
        return "unknown"

def build_graph():
    g = StateGraph(State)
    g.add_node("classify", classify_with_llM)
    g.add_node("flight_check", flight_check_node)
    g.add_node("book_flight", book_flight_node)
    g.add_node("cancel_flight",cancel_flight_node)
    g.add_node("response",response_node)

    g.set_entry_point("classify")

    g.add_conditional_edges(
        "classify",
        route_intent,
        {
            "flight_check": "flight_check",
            "book_flight": "book_flight",
            "cancel_flight": "cancel_flight",
            "unknown": "response",
            "exit": END,

        }
    )    
    g.add_edge("flight_check", "response")
    g.add_edge("book_flight", "response") 
    g.add_edge("cancel_flight", "response")

    return g.compile()


