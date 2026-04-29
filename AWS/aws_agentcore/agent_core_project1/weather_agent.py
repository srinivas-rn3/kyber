from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent,tool
from strands_tools import calculator
from strands.models import BedrockModel
import logging 

app = BedrockAgentCoreApp(debug=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define custom tool
@tool
def weather():
    """Get current weather"""
    return "Sunny"

# Configure model
model = BedrockModel(model_id="anthropic.claude-3-sonnet-20240229-v1:0")

# Create agent with tools
agent = Agent(
    model = model,
    tools = [calculator,weather],
    system_prompt= "You're a helpful assistant. You can do math calculations and tell the weather."
)
@app.entrypoint
def invoke(payload):
    """Agent entry point"""
    user_input = payload.get("prompt","Hello!")
    logger.info("User input: %s", user_input)
    response = agent(user_input)
    logger.info("Agent response: %s", response.message)
    return response.message['content'][0]['text']

if __name__ == "__main__":
    app.run()
