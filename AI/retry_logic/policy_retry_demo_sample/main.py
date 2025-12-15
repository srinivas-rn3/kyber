import random
from typing import TypedDict

from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy
from langchain_core.tools import tool

class State(TypedDict):
    policy_id: str
    eligibility: str | None

@tool
def external_policy_check(policy_id: str) -> bool:
    """Check policy eligibility from an external system."""
    print("Tool called")

    # Simulate failure
    if random.random() < 0.6:
        raise RuntimeError("External system failure")
    
    return policy_id.startswith("P")

def eligibility_node(state: State) -> State:
    print("Node Running")
    
    max_attempts = 3
    for attempt in range(max_attempts):
        try:
            print(f"Attempt {attempt + 1} of {max_attempts}")
            result = external_policy_check.invoke(state["policy_id"])
            print(f"Success on attempt {attempt + 1}")
            break
        except RuntimeError as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt == max_attempts - 1:
                print("All attempts failed, raising exception")
                raise
            print("Retrying...")

    return {
        **state,
        "eligibility": "ELIGIBLE" if result else "NOT ELIGIBLE"
    }

builder = StateGraph(State)

builder.add_node("check_eligibility", eligibility_node)
builder.set_entry_point("check_eligibility")
builder.set_finish_point("check_eligibility")

graph = builder.compile()

if __name__ == "__main__":
    result = graph.invoke({"policy_id": "PXXXX","eligibility": None})

    print("\n Final result")
    print(result)