def check_continue(state):
    ans = input("➕ Do you want to add another feedback? (yes/no): ").strip().lower()
    state['continue_feedback'] = ans == 'yes'
    return state
    