from langgraph.graph import END,StateGraph
from typing import TypedDict


# State: Track password attempts and status
class State(TypedDict,total=False):
    password: str # The password to be validated
    attempts: int  # Number of attempts made
    is_valid: bool  # Whether the password is valid
    message : str

# Node 1: Ask for password
def ask_password(state:State):
    attempts = state.get("attempts", 0)
    print(f"Attempts {attempts + 1} of 3")

    # In real app, you'd use input(). For demo, we'll simulate
    # For testing, we'll use the password from state
    password = state.get("password", "password")
    return {
        "password": password,
        "attempts": attempts + 1,
        "is_valid": False,
        "message": ""
    }

# Node 2: Check if password is correct
def check_password(state:State):
    password = state.get("password", "")
    correct_password = "secret_123"

    print(f"Checking password: '{password}'")

    if password == correct_password:
        print("Password is correct")
        return {
            "password": password,
            "attempts": state["attempts"],
            "is_valid": True,
            "message": "Access granted!"

        }
    else:
        return {
            "password": password,
            "attempts": state["attempts"],
            "is_valid": False,
            "message": "Wrong password!"
        }

# Node 3: Success message
def grant_access(state:State):
    print(f"\n{state['message']}")
    print(f"Welcome! you got it in {state['attempts']} attempt(s)!")
    return state

# Node 4: Locked out message
def lock_out(state:State):
    print(f"\nLOCKED OUT!")
    print("Too many attempts. Account locked!")
    return {
        "password": state["password"],
        "attempts": state["attempts"],
        "is_valid": False,
        "message": "Access Locked!"
    }

# Node 5: Prompt to try again
def try_again(state:State):
    attempts_left = 3 - state["attempts"]
    print(f"{state['message']}")
    print(f" You have {attempts_left} attempt(s) left")
    return state

# DECISION 1: Is password valid?
def check_validate(state:State):
    if state.get("is_valid", False):
        return "valid"
    else:
        return "invalid"

# DECISION 2: Can user try again?
def check_attempts(state:State):
    attempts = state.get("attempts", 0)
    if attempts >= 3:
        return "locked"
    else:
        return "retry"

# Build the graph
workflow = StateGraph(State)

# Add all nodes
workflow.add_node("ask", ask_password)
workflow.add_node("check", check_password)
workflow.add_node("success",grant_access)
workflow.add_node("locked",lock_out)
workflow.add_node("retry", try_again)

# Set starting point
workflow.set_entry_point("ask")

# Connect ask → check
workflow.add_edge("ask", "check")

# CONDITIONAL: After checking, is it valid?
workflow.add_conditional_edges(
    "check",
    check_validate,
    {
        "valid": "success", # Correct → Success
        "invalid": "retry"  # Wrong → Try again node
    }
)

# CONDITIONAL: After retry node, can they try again?
workflow.add_conditional_edges(
    "retry",
    check_attempts,
    {
        "retry": "ask",  # 🔄 LOOP BACK to ask!
        "locked": "locked" # Out of attempts → Locked
    }
)

# End nodes
workflow.add_edge("success", END)
workflow.add_edge("locked", END)

# Compile the app
app = workflow.compile()

# ============================================
# TEST CASES
#=============================================

print("="*70)
print("🔐 PASSWORD VALIDATOR - TEST SCENARIOS")
print("="*70)

print("\n" + "="*60)
print("Test 1: Correct on First Try")
print("="*70)
result1 = app.invoke({"password": "secret_123"})

print("\n" + "="*70)
print("TEST 2: Correct on Second Try")
print("="*70)
# Simulate multiple attempts by calling manually
test2_state ={"password": "wrong1", "attempts": 0}
for attempt_password in ["wrong1", "secret_123"]:
    test2_state["password"] = attempt_password
    result2 = app.invoke(test2_state)
    test2_state = result2
    if result2.get("is_valid"):
        break
print(f"\n Final State:{result2}")
