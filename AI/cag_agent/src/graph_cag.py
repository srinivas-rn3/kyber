import json
import os
from typing import TypedDict, Dict, Any
from langgraph.graph import StateGraph, END

from src.llm_bedrock import call_claude  # FIXED SPELLING


# ---------------------------------------------------
# STATE SHARED ACROSS GRAPH NODES
# ---------------------------------------------------
class CAGState(TypedDict):
    rules: Dict[str, Any]
    customer: Dict[str, Any]
    evaluation: str
    final_decision: str
    customer_id: str
    rule_id: str


# ---------------------------------------------------
# NODE 1: LOAD RULES + CUSTOMER (DYNAMIC)
# ---------------------------------------------------
def load_data(state: CAGState):

    customer_id = state["customer_id"]   # e.g., "cust_001"
    rule_id = state["rule_id"]           # e.g., "car_rules"

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Correct enterprise-style dynamic file loading:
    customer_path = os.path.join(base_dir, "data", "customers", f"{customer_id}.json")
    rules_path = os.path.join(base_dir, "data", "rules", f"{rule_id}.json")

    # Load dynamic customer
    with open(customer_path, "r") as f:
        state["customer"] = json.load(f)

    # Load dynamic rules
    with open(rules_path, "r") as f:
        state["rules"] = json.load(f)

    return state


# ---------------------------------------------------
# NODE 2: EVALUATE RULES USING CLAUDE (STRICT CAG)
# ---------------------------------------------------
def evaluate_rules(state: CAGState):

    prompt = f"""
You are a STRICT rule evaluator (CAG engine). No exceptions.

RULES:
{json.dumps(state["rules"], indent=2)}

CUSTOMER:
{json.dumps(state["customer"], indent=2)}

Return ONLY this JSON:
{{
  "eligible": true/false,
  "reason": "short explanation"
}}
"""

    result = call_claude(prompt)
    state["evaluation"] = result
    return state


# ---------------------------------------------------
# NODE 3: PREPARE FINAL DECISION
# ---------------------------------------------------
def final_answer(state: CAGState):

    result = json.loads(state["evaluation"])

    if result["eligible"]:
        state["final_decision"] = f"✅ ELIGIBLE: {result['reason']}"
    else:
        state["final_decision"] = f"❌ NOT ELIGIBLE: {result['reason']}"

    return state


# ---------------------------------------------------
# BUILD & COMPILE GRAPH
# ---------------------------------------------------
def build_graph():

    workflow = StateGraph(CAGState)

    workflow.add_node("load_data", load_data)
    workflow.add_node("evaluate_rules", evaluate_rules)
    workflow.add_node("final_answer", final_answer)

    workflow.set_entry_point("load_data")

    workflow.add_edge("load_data", "evaluate_rules")
    workflow.add_edge("evaluate_rules", "final_answer")
    workflow.add_edge("final_answer", END)

    return workflow.compile()
