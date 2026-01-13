import boto3
import json

client = boto3.client('bedrock-agent-runtime', region_name='us-east-1')

response = client.invoke_agent(
    agentId='AGENT12345',  # Replace with your actual agent ID (max 10 chars, alphanumeric only)
    agentAliasId='TSTALIASID',
    sessionId='testsession',
    inputText="What are the latest developments in AWS Bedrock?"
)

# Handle streaming response
content = []
if 'completion' in response:
    for chunk in response['completion']:
        if 'chunk' in chunk:
            content.append(chunk['chunk']['bytes'].decode('utf-8'))

# Parse and print the result
result = "".join(content)
print(result)
