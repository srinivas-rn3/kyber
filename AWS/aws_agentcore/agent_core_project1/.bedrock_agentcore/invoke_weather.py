import json,boto3 

agent_arn = "arn:aws:bedrock-agentcore:us-east-1:401038136415:runtime/weather_assistant-cBPTrzGdvd"

client =  boto3.client('bedrock-agentcore',region_name='us-east-1')

payload =  json.dumps({"prompt":"What's 100 / 57"}).encode()

response = client.invoke_agent_runtime(
     agentRuntimeArn=agent_arn,
     payload=payload
    )
content  = []
for chunk in response.get("response",[]):
    content.append(chunk.decode("utf-8"))

print(json.loads("".join(content)))
