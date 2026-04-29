def get_feedback(state):
    fb = input("📝 Please enter your feedback: ").strip()
    
    # Make a copy of the list (safe way)

    feedbacks = list(state.get("feedbacks",[]))

    if fb:
        feedbacks.append(fb)
    
    # 🧠 Return a new state object instead of mutating

    new_state = dict(state)
    new_state["feedbacks"] = feedbacks

    #print(f"🧾 Saved feedbacks so far: {new_state['feedbacks']}")  # debug line
    return new_state