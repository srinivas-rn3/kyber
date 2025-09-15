import boto3
import json

# 1. Create a client for the Bedrock Runtime service
# Make sure the region (e.g., 'us-east-1') matches the region where you requested model access.
client = boto3.client('bedrock-runtime', region_name='ap-south-1')

# 2. Choose which model you want to use
# Find the correct Model ID in the Bedrock console under "Provisioned models" or "Foundation models"
model = 'anthropic.claude-3-haiku-20240307-v1:0'

# 3. Create your message in the Converse API format
messages = [{
    "role":"user",
    "content":[{"text":"What is the capital of France"}]
}]

# 4. Call the Converse API
response =  client.converse(
    modelId = model,
    messages = messages 
)

# 5. Extract and print the response
answer = response['output']['message']['content'][0]['text']
print(answer)