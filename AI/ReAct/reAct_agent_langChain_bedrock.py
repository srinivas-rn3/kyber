from langchain_aws import ChatBedrock
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
import time
from botocore.exceptions import ClientError


# -----------------------------
# 1. Setup Bedrock LLM
# -----------------------------

llm = ChatBedrock(
    model_id = "anthropic.claude-3-haiku-20240307-v1:0",
    region_name = "ap-south-1"
)

# -----------------------------
# 2. Define Tools
# -----------------------------

def calculator(expr: str) -> str:
    """simple math calculator"""
    try:
        # Remove quotes if present
        expr = expr.strip("'\"")
        result = eval(expr)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

tools = [Tool(
    name="Calculator",
    func=calculator,
    description="Use this to solve math expressions. Input should be a string like '2+3*5'. Only use this once per calculation."
)]

# -----------------------------
# 3. Initialize ReAct Agent
# -----------------------------

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # ReAct loop under the hood
    verbose=True,  # <-- prints Thought, Action, Observation automatically
    max_iterations=3,  # Limit iterations to prevent infinite loops
    max_execution_time=30,  # Timeout after 30 seconds
    early_stopping_method="generate"  # Stop when final answer is generated
)

# -----------------------------
# 4. Run Queries with Error Handling
# -----------------------------

def run_agent_with_retry(agent, query, max_retries=3, delay=5):
    """Run agent with retry logic for throttling errors"""
    for attempt in range(max_retries):
        try:
            response = agent.run(query)
            return response
        except ClientError as e:
            if e.response['Error']['Code'] == 'ThrottlingException':
                if attempt < max_retries - 1:
                    print(f"Throttling detected. Waiting {delay} seconds before retry {attempt + 1}...")
                    time.sleep(delay)
                    delay *= 2  # Exponential backoff
                else:
                    print("Max retries reached. Please wait before trying again.")
                    raise
            else:
                raise
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

try:
    response = run_agent_with_retry(agent, 'What is 9*8*(9/2)')
    print("\nFinal Answer:", response)
except Exception as e:
    print(f"Agent execution failed: {e}")
    