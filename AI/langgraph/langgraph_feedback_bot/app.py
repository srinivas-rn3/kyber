from graph.main_graph import build_graph

def main():
    app =  build_graph()
    print("💬 Feedback Bot started! Type your feedback when asked.\n")

    # Empty starting state
    state = {
        "feedbacks":[],
        "continue_feedback": True
        }

    app.invoke(state)

if __name__ == "__main__":
    main()
