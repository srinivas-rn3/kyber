from langgraph.graph import StateGraph, END
from typing import TypedDict
from nodes.greet_node import greet
from nodes.feedback_node import get_feedback
from nodes.check_continue_node import check_continue
from nodes.summary_node import show_summary

# ----- STATE -----
class State(TypedDict):
    continue_feedback: bool
    feedbacks: list

# ----- ROUTER FUNCTION -----
def route_continue(state: State):
    return "feedback" if state['continue_feedback'] else "summary"

# ----- BUILD GRAPH -----
def build_graph():
    g = StateGraph(State)

    g.add_node("greet", greet)
    g.add_node("feedback", get_feedback)
    g.add_node("check", check_continue)
    g.add_node("summary", show_summary)

    g.set_entry_point("greet")

    #Flow
    g.add_edge("greet", "feedback")
    g.add_edge("feedback", "check")

    # Loop based on user response
    g.add_conditional_edges(
        "check",
        route_continue,
        {
            "feedback": "feedback",
            "summary": "summary"
        }
    )
    return g.compile()
    

  