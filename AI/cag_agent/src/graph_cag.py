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

    customer_id = state["customer_id"]

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # path to customer file
    customer_path = os.path.join(base_dir, "data", "customers", f"{customer_id}.json")

    # ---- VALIDATE CUSTOMER FILE ----
    if not os.path.exists(customer_path):
        raise ValueError(f"❌ Customer '{customer_id}' does not exist. Please try again.")

    # ---- LOAD CUSTOMER JSON ----
    with open(customer_path, "r") as f:
        customer_data = json.load(f)

    state["customer"] = customer_data

    # -------- POLICY TYPE RESOLUTION LOGIC ----------
    # 1. If override exists → use it
    override = state.get("policy_type_override")

    if override:
        policy_type = override

    # 2. Else if single policy_type exists in JSON → use that
    elif customer_data.get("policy_type"):
        policy_type = customer_data["policy_type"]

    # 3. Else if policy_types list exists → take first one
    elif customer_data.get("policy_types"):
        policy_type = customer_data["policy_types"][0]

    # 4. Else → no policy_type found
    else:
        raise ValueError(f"❌ No policy_type found for customer '{customer_id}'.")

    # Build rule file name
    rule_file = f"{policy_type}_rules.json"

    rule_path = os.path.join(base_dir, "data", "rules", rule_file)

    # ---- VALIDATE RULE FILE ----
    if not os.path.exists(rule_path):
        raise ValueError(f"❌ Rule file not found for policy_type '{policy_type}'.")

    # ---- LOAD RULE FILE ----
    with open(rule_path, "r") as f:
        rules_data = json.load(f)

    state["rules"] = rules_data

    return state

# ---------------------------------------------------
# NODE 2: EVALUATE RULES USING CLAUDE (STRICT CAG)
# ---------------------------------------------------
def evaluate_rules(state: CAGState):

    rules = state["rules"]
    customer = state["customer"]

    prompt = f"""
You are a STRICT enterprise rule engine (CAG). 
You must evaluate ALL rules precisely. No guessing.

RULE SET (JSON):
{json.dumps(rules, indent=2)}

CUSTOMER (JSON):
{json.dumps(customer, indent=2)}

Each rule has:
- id
- name
- description (condition in natural language)
- severity: "critical" or "medium" or "low"

1. For EACH rule:
   - Decide if it PASSES or FAILS for this customer.
   - Give a short reason.

2. Then decide overall eligibility:
   - If ANY critical rule FAILS → eligible = false.
   - If only non-critical rules fail → eligible = true but with warnings.

Return ONLY this JSON (no extra text):

{{
  "eligible": true/false,
  "failed_rules": [
    {{"id": "R1", "reason": "expired_days 45 > allowed 30", "severity": "critical"}}
  ],
  "passed_rules": [
    "R2",
    "R3"
  ],
  "summary": "Short natural language explanation combining key reasons."
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

    eligible = result["eligible"]
    summary = result.get("summary", "")
    failed_rules = result.get("failed_rules", [])
    passed_rules = result.get("passed_rules", [])

    # Extract failed rule details (if any)
    if failed_rules:
        fr = failed_rules[0]  # first failed rule
        rule_id = fr["id"]
        rule_reason = fr["reason"]
        severity = fr["severity"]
    else:
        rule_id = None
        rule_reason = None
        severity = None

    # -------------- NOT ELIGIBLE -----------------
    if not eligible:
        state["final_decision"] = f"""
❌ NOT ELIGIBLE

🔎 Failed Rule: {rule_id} – {severity.upper()}
Reason: {rule_reason}

📌 What You Should Do Next:
- Customer must follow the reinstatement process OR apply for a new policy.
        """.strip()
        return state

    # -------------- ELIGIBLE WITH WARNINGS -----------------
    if eligible and failed_rules:
        state["final_decision"] = f"""
⚠️ ELIGIBLE WITH WARNINGS

Passed Rules: {', '.join(passed_rules)}

Issues Found:
{summary}

📌 Recommendation:
- Customer can renew, but medium/low severity issues must be addressed.
        """.strip()
        return state

    # -------------- FULLY ELIGIBLE -----------------
    state["final_decision"] = f"""
✅ ELIGIBLE

All rules passed successfully.
Summary: {summary}
    """.strip()

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
