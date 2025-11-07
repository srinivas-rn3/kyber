def flight_check_node(state):
    destination = state.get("destination","").title()
    date = state.get("date", "today")

    fake_schedule = {
        "Singapore": "Flight AI302 – 10:45 AM tomorrow",
        "Tokyo": "Flight JL746 – 8:00 PM Friday",
        "Paris": "Flight AF217 – 6:30 AM next Tuesday",
    }
    result  = fake_schedule.get(destination,f"No flights found to {destination} {date}.")
    print(f"{result}")
    state["flight_result"] = result
    return state
    
