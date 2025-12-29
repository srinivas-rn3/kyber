"""
Customer Support Agent - Main Entrypoint
This agent helps customers with account queries, order tracking, and FAQs
"""
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent, tool
from strands.models import BedrockModel
from tools.support_tools import check_order_status, get_account_info, search_faq
from config.settings import MODEL_ID, SYSTEM_PROMPT
import logging

# Initialize AgentCore app
app = BedrockAgentCoreApp(debug=True)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure the model
model = BedrockModel(
    model_id=MODEL_ID,
    temperature=0.7,
    max_tokens=1024
)

# Create agent with tools
agent = Agent(
    model=model,
    tools=[
        check_order_status,
        get_account_info,
        search_faq
    ],
    system_prompt=SYSTEM_PROMPT
)

@app.entrypoint
def invoke(payload):
    """
    Main entry point for the agent.
    Called when agent receives a request from user or API.
    
    Args:
        payload (dict): Input data with structure:
            {
                "prompt": "user message",
                "user_id": "optional user identifier",
                "session_id": "optional session identifier"
            }
    
    Returns:
        dict: Response with agent's answer
    """
    # Extract user input
    user_message = payload.get("prompt", "")
    user_id = payload.get("user_id", "anonymous")
    session_id = payload.get("session_id", "default")
    
    logger.info(f"Received request from user: {user_id}, session: {session_id}")
    logger.info(f"User message: {user_message}")
    
    # Validate input
    if not user_message:
        return {
            "response": "Please provide a message.",
            "error": "Empty prompt"
        }
    
    try:
        # Invoke agent with user message
        result = agent(user_message)
        
        # Extract response text
        response_text = result.message['content'][0]['text']
        
        logger.info(f"Agent response: {response_text}")
        
        return {
            "response": response_text,
            "user_id": user_id,
            "session_id": session_id,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        return {
            "response": "I apologize, but I encountered an error processing your request.",
            "error": str(e),
            "status": "error"
        }

# Local testing support
if __name__ == "__main__":
    logger.info("Starting agent in local mode on port 8080...")
    app.run()
