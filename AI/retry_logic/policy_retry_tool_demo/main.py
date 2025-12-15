from langgraph.graph import StateGraph, END
from langchain_aws import ChatBedrock
from tools import check_expiry, check_amount
from logic.data_loader import load_json
import time
import logging
from typing import TypedDict, Any

# ----------------------------
# STATE
# ----------------------------
class State(TypedDict):
    customer: dict
    rules: dict
    evaluation: Any
    decision: str

# Initialize LLM with error handling
try:
    llm = ChatBedrock(model_id="anthropic.claude-3-haiku-20240307-v1:0",
                     region_name="ap-south-1")
    # Bind tools to the LLM
    llm_with_tools = llm.bind_tools([check_expiry, check_amount])
except Exception as e:
    print(f"Warning: Could not initialize ChatBedrock: {e}")
    llm = None
    llm_with_tools = None

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
# NODE 2: llm_evaluator  (with retry)
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
def llm_evaluator(state: State):
    print("Evaluating policy...")
    if llm_with_tools is None:
        print("Using fallback evaluation (no LLM available)")
        # Fallback to simple evaluation if LLM is not available
        customer = state['customer']
        rules = state['rules']
        
        expiry_check = check_expiry.invoke({"days": customer['days_expired'], "max_allowed": rules['max_expiry_days']})
        amount_check = check_amount.invoke({"amount": customer['amount_due'], "max_allowed": rules['max_amount_due']})
        
        evaluation = {
            "policy_expired": expiry_check,
            "amount_exceeded": amount_check,
            "recommendation": "REJECT" if (expiry_check or amount_check) else "APPROVE"
        }
        state['evaluation'] = evaluation
    else:
        print("Using LLM evaluation")
        prompt = f"""
        Analyze customer policy based on rules.

    Customer: {state['customer']}
    Rules: {state['rules']}

    Based on the data, determine if the policy should be approved or rejected.
    Use the available tools to check expiry and amount limits.
    """
        response = llm_with_tools.invoke(prompt)
        state['evaluation'] = response
    
    return state

# ----------------------------
# NODE 3: finalize
# ----------------------------

def finalize(state):
    state['decision'] = f"Final Decision -> {state['evaluation']}"
    return state

# ----------------------------
# BUILD GRAPH
# ----------------------------
graph = StateGraph(State)
graph.add_node("load_data", load_data)
graph.add_node("llm_evaluator", llm_evaluator)
graph.add_node("finalize", finalize)

graph.set_entry_point("load_data")
graph.add_edge("load_data", "llm_evaluator")
graph.add_edge("llm_evaluator", "finalize")
graph.add_edge("finalize", END)

app = graph.compile()

# ----------------------------
# RUN
# ----------------------------

if __name__ == "__main__":
    result = app.invoke({})
    print(result['decision'])