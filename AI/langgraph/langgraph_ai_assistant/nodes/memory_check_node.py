def memory_check_node(state):
    """
    Checks if city is missing. If missing, tries to reuse last city from history.
    If still missing, asks the user for a city.
    """

    city =  state.get('city',"").strip()
    history = state.get('history', [])

    # ✅ 1. If city already present, nothing to do
    if city:
        return state

    # ✅ 2. Try to find the last mentioned city in history
    last_city = None
    for msg in reversed(history):
        if msg['role'] == 'user' and "weather in" in msg['content'].lower():
            # crude extraction
            parts = msg['content'].split("in")
            if len(parts) > 1:
                last_city = parts[1].strip(" ?. ")
                break
        
        if last_city:
            print(f"🧠 Using last mentioned city from memory: {last_city}")
            state['city'] = input(">> ").strip()
            return state
        
            