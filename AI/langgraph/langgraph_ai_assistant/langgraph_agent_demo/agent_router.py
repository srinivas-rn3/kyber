def agent_router(state):
    """Route user input to appropriate node"""
    msg = state["message"].lower().strip()
    
    if "add feedback" in msg:
        return "add"
    elif "show" in msg or "list" in msg or "feedback" in msg:
        return "show"
    elif msg in ["exit", "quit", "bye"]:
        return "exit"
    else:
        return "unknown"
