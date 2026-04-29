def cancel_flight_node(state):
    airline = state.get("airlines","")
    dest = state.get("destinations", "")
    msg = f"Your {airline or 'scheduled'} flight to {dest or 'the mentined '} has been cancelled."
    print(msg)
    state['flight_result'] = msg
    return state
    