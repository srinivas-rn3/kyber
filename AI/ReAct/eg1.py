import boto3
import json

# --- Setup Bedrock Runtime client ---
client = boto3.client("bedrock-runtime", region_name="ap-south-1")  # change if needed

# --- Define Tools ---
def calculator(expr):
    try:
        return str(eval(expr))
    except:
        return "Error"

def search(query):
    return f"Fake search result for: {query}"

tools = {
    "Calculator": calculator,
    "Search": search
}

# --- ReAct Agent ---
def react_agent(question):
    history = ""
    for step in range(5):  # limit steps
        # Call Claude Haiku
        response = client.invoke_model(
            modelId="anthropic.claude-3-haiku-20240307-v1:0",
            body=json.dumps({
                "max_tokens": 300,
                "messages": [
                    {"role": "system", "content": "You are a ReAct agent. You can use tools: Calculator(expr), Search(query)."},
                    {"role": "user", "content": history + f"\nQuestion: {question}"}
                ]
            })
        )
        
        output = json.loads(response["body"].read())["content"][0]["text"]
        print(f"Model:\n{output}\n")

        # If model calls a tool
        if "Action:" in output:
            try:
                action_line = output.split("Action:")[-1].strip()
                tool_name, arg = action_line.split("(", 1)
                tool_name = tool_name.strip()
                arg = arg[:-1]  # remove closing )
                obs = tools[tool_name](arg)
            except:
                obs = "Tool error"
            
            history += f"{output}\nObservation: {obs}\n"
        else:
            break

# --- Run Example ---
react_agent("What is 2 + 3 * 5?")
