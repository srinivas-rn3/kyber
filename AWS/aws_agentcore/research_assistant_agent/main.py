from agent import graph
from bedrock_agentcore import BedrockAgentCoreApp


app = BedrockAgentCoreApp()

@app.entrypoint()
def handler(event, context):
    # Extract user prompt from event
    user_input = event.get("prompt", "Hello")

    # Invoke graph
    result = graph.invoke({
        "messages": [("user", user_input)]
    })
    # Return the final response
    final_message = result["messages"][-1].content

    return {
        "response": final_message
    }

