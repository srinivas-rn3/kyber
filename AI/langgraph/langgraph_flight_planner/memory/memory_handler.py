def update_memory(state, history):
    msg = state.get("message", "")
    if msg:
        history.append({"role": "user", "content": msg})
    state["history"] = history[-5:]
    return state
