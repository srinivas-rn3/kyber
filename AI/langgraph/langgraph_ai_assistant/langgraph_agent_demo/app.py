from langgraph.graph import StateGraph, END
from typing import TypedDict

from tools.add_feedback import add_feedback
from tools.show_feedback import show_feedback
from agent_router import agent_router


# ==== STATE ====
class State(TypedDict):
    message: str


# ==== INPUT NODE ====
def get_input(state):
    user_msg = input("You: ")
    state["message"] = user_msg
    return state


# ==== FALLBACK ====
def fallback(state):
    print("🤔 Sorry, I didn't understand that.")
    return state


# ==== BUILD AGENT ====
def build_agent():
    g = StateGraph(State)

    g.add_node("input", get_input)
    g.add_node("add", add_feedback)
    g.add_node("show", show_feedback)
    g.add_node("unknown", fallback)

    g.set_entry_point("input")

    g.add_conditional_edges(
        "input",
        agent_router,
        {
            "add": "add",
            "show": "show",
            "exit": END,
            "unknown": "unknown"
        }
    )

    # Loop back to input
    g.add_edge("add", "input")
    g.add_edge("show", "input")
    g.add_edge("unknown", "input")

    return g.compile()


if __name__ == "__main__":
    app = build_agent()
    app.invoke({"message": ""})
