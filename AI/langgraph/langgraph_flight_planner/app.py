from graph.main_graph import build_graph

def main():
    app = build_graph()
    print("🛫 Travel Flight Planner ready! Type 'exit' to quit.")
    while True:
        msg = input("You: ")
        if msg.lower() in ["exit", "quit", "q", "bye"]:
            print("👋 Goodbye!")
            break
        app.invoke({"message":msg,"history":[]})

if __name__ == "__main__":
    main()
