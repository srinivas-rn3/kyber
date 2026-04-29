def agent_router(state):
    msg = state["message"].lower()

    if msg.startswith("add feedback"):
        return "add"

    if "show" in msg or "list" in msg:
        return "show"

    if "exit" in msg:
        return "exit"

    return "unknown"
