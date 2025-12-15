from langgraph.graph import StateGraph, END
from tools import check_expiry, check_amount
from logic.data_loader import load_json
import time
import logging
from typing import TypedDict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)

# ----------------------------
# STATE
# ----------------------------
class State(TypedDict):
    customer: dict
    rules: dict
    evaluation: Any
    decision: str

# ----------------------------
# NODE 1: load_data
# ----------------------------
def load_data(state):
    print("Loading data...")
    state['customer'] = load_json("customer.json")
    state['rules'] = load_json("rules.json")
    print(f"Loaded customer: {state['customer']}")
    print(f"Loaded rules: {state['rules']}")
    return state

# ----------------------------
# NODE 2: simple_evaluator (with retry)
# ----------------------------
def retry_with_policy(func, max_retries=3, delay=2):
    """Custom retry decorator"""
    def wrapper(*args, **kwargs):
        for attempt in range(max_retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt == max_retries - 1:
                    logging.error(f"Failed after {max_retries} attempts: {e}")
                    raise e
                logging.warning(f"Attempt {attempt + 1} failed: {e}. Retrying in {delay} seconds...")
                time.sleep(delay)
    return wrapper

@retry_with_policy
def simple_evaluator(state: State):
    print("Evaluating policy...")
    customer = state['customer']
    rules = state['rules']
    
    # Simple evaluation logic
    expiry_check = check_expiry.invoke({"days": customer['days_expired'], "max_allowed": rules['max_expiry_days']})
    amount_check = check_amount.invoke({"amount": customer['amount_due'], "max_allowed": rules['max_amount_due']})
    
    evaluation = {
        "policy_expired": expiry_check,
        "amount_exceeded": amount_check,
        "recommendation": "REJECT" if (expiry_check or amount_check) else "APPROVE"
    }
    
    state['evaluation'] = evaluation
    return state

# ----------------------------
# NODE 3: finalize
# ----------------------------
def finalize(state):
    state['decision'] = f"Final Decision -> {state['evaluation']['recommendation']}"
    return state

# ----------------------------
# BUILD GRAPH
# ----------------------------
graph = StateGraph(State)
graph.add_node("load_data", load_data)
graph.add_node("simple_evaluator", simple_evaluator)
graph.add_node("finalize", finalize)

graph.set_entry_point("load_data")
graph.add_edge("load_data", "simple_evaluator")
graph.add_edge("simple_evaluator", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

# ----------------------------
# RUN
# ----------------------------
if __name__ == "__main__":
    result = app.invoke({})
    print(f"\nResult: {result['decision']}")
    print(f"Full evaluation: {result['evaluation']}")