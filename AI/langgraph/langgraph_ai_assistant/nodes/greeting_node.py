def greet(state):
    """Greeting node that welcomes the user"""
    print("Hello! I'm your AI assistant. How can I help you today?")
    
    # Get user input
    user_message = input("You: ")
    state['message'] = user_message
    
    return state