from memory.memory import feedbacks

def show_feedback(state):
    print("\n📝 All Feedbacks:")
    
    if not feedbacks:
        print("No feedbacks yet.")
    else:
        for i, fb in enumerate(feedbacks, start=1):
            print(f"{i}. {fb}")

    return state
