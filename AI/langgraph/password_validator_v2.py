from langgraph.graph import END, StateGraph
from typing import TypedDict

# ===============================
# Define the state
# ===============================
class State(TypedDict, total=False):
    password: str
    attempts: int
    is_valid: bool
    message: str


# ===============================
# Nodes
# ===============================

# Node 1: Ask for password
def ask_password(state: State):
    attempts = state.get("attempts", 0)
    print(f"Attempts {attempts + 1} of 3")

    # Simulated password (in real use, you'd collect input)
    password = state.get("password", "password")

    return {
        "password": password,
        "attempts": attempts + 1,
        "is_valid": False,
        "message": ""
    }


# Node 2: Check if password is correct
def check_password(state: State):
    password = state.get("password", "")
    correct_password = "secret_123"

    print(f"Checking password: '{password}'")

    if password == correct_password:
        print("Password is correct ✅")
        return {
            "password": password,
            "attempts": state["attempts"],
            "is_valid": True,
            "message": "Access granted!"
        }
    else:
        print("Password is wrong ❌")
        return {
            "password": password,
            "attempts": state["attempts"],
            "is_valid": False,
            "message": "Wrong password!"
        }


# Node 3: Success
def grant_access(state: State):
    print(f"\n{state['message']}")
    print(f"Welcome! You got it in {state['attempts']} attempt(s) 🎉")
    return state


# Node 4: Locked out
def lock_out(state: State):
    print("\nLOCKED OUT! 🔒")
    print("Too many attempts. Account locked!")
    return {
        "password": state["password"],
        "attempts": state["attempts"],
        "is_valid": False,
        "message": "Access Locked!"
    }


# Node 5: Retry
def try_again(state: State):
    attempts_left = 3 - state["attempts"]
    print(f"{state['message']}")
    print(f"You have {attempts_left} attempt(s) left. Try again.\n")
    return state


# ===============================
# Single merged decision function
# ===============================
def check_status(state: State):
    if state.get("is_valid", False):
        return "valid"
    elif state.get("attempts", 0) >= 3:
        return "locked"
    else:
        return "retry"


# ===============================
# Build the workflow
# ===============================
workflow = StateGraph(State)

workflow.add_node("ask", ask_password)
workflow.add_node("check", check_password)
workflow.add_node("success", grant_access)
workflow.add_node("locked", lock_out)
workflow.add_node("retry", try_again)

workflow.set_entry_point("ask")

workflow.add_edge("ask", "check")

workflow.add_conditional_edges(
    "check",
    check_status,
    {
        "valid": "success",
        "retry": "retry",
        "locked": "locked"
    }
)

workflow.add_edge("retry", "ask")
workflow.add_edge("success", END)
workflow.add_edge("locked", END)

# Compile
app = workflow.compile()


# ===============================
# Test Cases
# ===============================
print("=" * 70)
print("🔐 PASSWORD VALIDATOR - TEST SCENARIOS")
print("=" * 70)

# Test 1
print("\n" + "=" * 60)
print("Test 1: Correct on First Try")
print("=" * 60)
result1 = app.invoke({"password": "secret_123"})

# Test 2
print("\n" + "=" * 60)
print("Test 2: Correct on Second Try")
print("=" * 60)
test2_state = {"password": "wrong1", "attempts": 0}
for attempt_password in ["wrong1", "secret_123"]:
    test2_state["password"] = attempt_password
    result2 = app.invoke(test2_state)
    test2_state = result2
    if result2.get("is_valid"):
        break

print(f"\nFinal State: {result2}")

# Test 3
print("\n" + "=" * 60)
print("Test 3: Locked After 3 Wrong Attempts")
print("=" * 60)
test3_state = {"password": "bad", "attempts": 0}
for attempt_password in ["bad", "wrong", "fail"]:
    test3_state["password"] = attempt_password
    result3 = app.invoke(test3_state)
    test3_state = result3
    if result3.get("message") == "Access Locked!":
        break

print(f"\nFinal State: {result3}")
