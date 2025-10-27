from langchain_aws import ChatBedrock
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import time
from botocore.exceptions import ClientError

# -----------------------------
# 1. Setup Bedrock LLM
# -----------------------------

llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="ap-south-1"
)

# -----------------------------
# 2. Define Tools
# -----------------------------

def calculator(expression: str) -> str:
    """Evaluates mathematical expressions and returns the result."""
    try:
        # Clean the input
        expression = expression.strip().strip("'\"")
        print(f"Calculating: {expression}")
        
        # Evaluate the expression
        result = eval(expression)
        return f"The result is: {result}"
    except Exception as e:
        return f"Error calculating {expression}: {str(e)}"

tools = [
    Tool(
        name="Calculator",
        func=calculator,
        description="Use this tool to perform mathematical calculations. Input a mathematical expression like '9*8*(9/2)' and get the numerical result."
    )
]

# -----------------------------
# 3. Initialize ReAct Agent
# -----------------------------

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    max_iterations=5,
    max_execution_time=60,
    early_stopping_method="generate"
)

# -----------------------------
# 4. Run with Error Handling
# -----------------------------

def run_with_backoff(query, max_retries=3):
    """Run agent with exponential backoff for throttling"""
    for attempt in range(max_retries):
        try:
            print(f"\n=== Attempt {attempt + 1} ===")
            response = agent.invoke({"input": query})
            return response["output"]
        except Exception as e:
            if "ThrottlingException" in str(e) or "Too many requests" in str(e):
                if attempt < max_retries - 1:
                    wait_time = (2 ** attempt) * 5  # 5, 10, 20 seconds
                    print(f"Throttling detected. Waiting {wait_time} seconds...")
                    time.sleep(wait_time)
                else:
                    print("Max retries reached due to throttling.")
                    return "Error: Too many requests to Bedrock. Please try again later."
            else:
                print(f"Error: {e}")
                return f"Error: {e}"

if __name__ == "__main__":
    query = "What is 9*8*(9/2)?"
    result = run_with_backoff(query)
    print(f"\n=== Final Result ===")
    print(result)