from memory.memory import feedbacks

def add_feedback(state):
    fb = state["message"].replace("add feedback", "").strip()
    feedbacks.append(fb)
    print(f"🟢 Saved feedback: {fb}")
    return state
