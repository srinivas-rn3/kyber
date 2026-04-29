import sys
import os

# Ensure the mini-agent directory is on the path regardless of how the script is invoked
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agent import MiniAgent


def main():
    agent = MiniAgent()
    print("Mini Bedrock AI Agent started. Type 'exit' to quit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        try:
            response = agent.execute(user_input)
            print(f"Agent: {response}")
        except Exception as e:
            print(f"Agent error: {e}")


if __name__ == "__main__":
    main()
