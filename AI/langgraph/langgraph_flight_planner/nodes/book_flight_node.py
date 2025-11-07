def book_flight_node(state):
    dest = state.get('destination',"")
    date = state.get('date', "")
    time = state.get('time', "") 


    if not dest:
        print("✈️ Please tell me your destination city.")
        return state
    
    result = f"Your flight to {dest} has been booked for {date or 'today'} at {time}."
    print(result)
    state['flight_result'] = result
    return state