import boto3,json 

## --- Bedrock Client ---
client  =  boto3.client("bedrock-runtime",region_name="ap-south-1")


# --- Tools available to the agent ---
def calculator(expr):
    try:
        return str(eval(expr))
    except:
        return "Error"

tools = {"calculator":calculator}

# --- ReAct Prompt Template ---
def build_prompt(question,history):
    return f"""
You are a reasoning agent. 
You can use these tools: calculator(expr).

Use the format:
Thought: what you think
Action: tool(input)
Observation: result
Final Answer: your answer

{history}
User Question: {question}
"""
# --- ReAct Loop ---
def react_agent(question):
    history = ""
    while True:
        prompt = build_prompt(question,history)

        response = client.converse(
            modelId = "anthropic.claude-3-haiku-20240307-v1:0",
            messages = [{"role":"user","content":[{"text":prompt}]}],
            inferenceConfig = {"maxTokens":300}
        )
        
        output = response['output']['message']['content'][0]['text']

        print("---Model Output---")
        print(output)

        if "Action:" in  output:
            try:
                action_line = output.split("Action:")[-1].strip()
                tool_name,arg =  action_line.split("(",1)
                tool_name = tool_name.strip()
                arg = arg[:-1]
                obs = tools[tool_name](arg)
            except Exception as e:
                obs = f"Tools error: {e}"

            history += f"{output}\nObservation: {obs}\n"
        else:
            break
    
    return output

####RUN###
print(react_agent("What is 2+3*5?"))
