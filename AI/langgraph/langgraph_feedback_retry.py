from langgraph.graph import StateGraph, END
from typing import TypedDict

# ============================================
# 🧱 Step 1: Define State
# --------------------------------------------
# Keeps track of user feedback, attempt count, and continuation choice.
# ============================================
class State(TypedDict):
    feedback: str
    attempts: int
    continue_feedback: bool


# ============================================
# 🧩 Step 2: Define Nodes
# ============================================

def start(state: State):
    print("👋 Hi! We'd love your feedback on our service.")
    state["attempts"] = 0
    state["continue_feedback"] = True
    return state


def ask_feedback(state: State):
    print("\nHow was your experience with us today? (good/bad)")
    state["feedback"] = input(">> ").strip().lower()
    state["attempts"] += 1
    return state


def check_feedback(state: State):
    if "good" in state["feedback"]:
        print("\n😊 That’s great to hear! Thank you for your feedback.")
        state["continue_feedback"] = False
    else:
        print("\n😔 Sorry to hear that.")
        if state["attempts"] < 3:
            print("Would you like to share more details? (yes/no)")
            ans = input(">> ").strip().lower()
            state["continue_feedback"] = ans == "yes"
        else:
            print("\nYou’ve reached the maximum feedback attempts.")
            state["continue_feedback"] = False
    return state


def thank_you(state: State):
    print("\n🙏 Thanks for taking the time to share your thoughts. Have a great day!")
    return state


# ============================================
# ⚙️ Step 3: Decision Function
# --------------------------------------------
# This decides whether to loop again or end.
# ============================================
def decide_next(state: State):
    if state["continue_feedback"]:
        return "again"
    else:
        return "end"


# ============================================
# 🧩 Step 4: Build Graph
# ============================================

workflow = StateGraph(State)

workflow.add_node("start", start)
workflow.add_node("ask_feedback", ask_feedback)
workflow.add_node("check_feedback", check_feedback)
workflow.add_node("thank_you", thank_you)

workflow.set_entry_point("start")

# Define edges
workflow.add_edge("start", "ask_feedback")
workflow.add_edge("ask_feedback", "check_feedback")

# Conditional edges for loop control
workflow.add_conditional_edges(
    "check_feedback",
    decide_next,
    {
        "again": "ask_feedback",  # Loop if user wants to continue
        "end": "thank_you",       # Stop if user is done
    }
)

# ============================================
# 🚀 Step 5: Compile and Run
# ============================================
app = workflow.compile()
app.invoke({})
