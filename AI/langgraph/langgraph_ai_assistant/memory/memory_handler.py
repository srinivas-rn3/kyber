# Very simple memory store — can be expanded to Redis or DynamoDB later
def update_memory(state, history):
    """
    Keeps track of recent user and assistant messages.
    """
    user_msg = state.get("messages","")
    if user_msg:
        history.append({"role": "user", "content": user_msg})
    
    # Optional: store the last weather result (assistant reply)
    if "weather_result" in state and state["weather_result"]:
        history.append({"role": "assistant", "content": state["weather_result"]})
    
    # Keep only the last 6 turns
    state["history"] = history[-6:]
    return state



