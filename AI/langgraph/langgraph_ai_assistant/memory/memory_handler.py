# Very simple memory store — can be expanded to Redis or DynamoDB later
def update_memory(state, history):
    message = state.get('message')
    if message:
        history.append(message)
    state['history'] = history[-5:]  # Keep last 5 messages
    return state

