import os
from dotenv import load_dotenv

# Load .env first, overriding any system env vars
load_dotenv(
    dotenv_path=os.path.join(os.path.dirname(__file__), ".env"),
    override=True
)

# Force override system env vars that dotenv can't override
os.environ["MODEL_ID"] = "us.anthropic.claude-3-5-sonnet-20241022-v2:0"
os.environ["LANGSMITH_TRACING"] = "false"

from graph_agent import build_graph


def main():
    graph = build_graph()
    print("Mini LangGraph Agent started. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        initial_state = {
            "user_input": user_input,
            "prompt": "",
            "llm_output": "",
            "actions": [],
            "results": [],
            "final_response": "",
        }

        try:
            final_state = graph.invoke(initial_state)
            print(f"Agent: {final_state['final_response']}")
        except Exception as exc:
            print(f"Agent error: {exc}")


if __name__ == "__main__":
    main()