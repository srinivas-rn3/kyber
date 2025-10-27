import boto3, time 

# 1. Setup the client for Mumbai with Claude Haiku
client = boto3.client('bedrock-runtime', region_name='ap-south-1')
model_id = 'anthropic.claude-3-haiku-20240307-v1:0'

# 2. Create your message
messages = [{
"role":"user",
"content":[{"text":"Explain the concept of neural network in simple terms."}]
}]
print("Haiku:Thinking....\n")
print("Response: ", end="", flush=True) # 'end=""' prevents newline, 'flush=True' shows text immediately

# 3. Call the ConverseStream API
stream = client.converse_stream(
    modelId=model_id,
    messages=messages,
    inferenceConfig={'maxTokens': 300}
)

# 4. Process the streaming response
usage_info = None
for event in stream['stream']:
    # Check if the event contains a new text chunk
    if "contentBlockDelta" in event:
        delta = event['contentBlockDelta']
        # Print the new text chunk as it comes in, without a newline
        print(delta['delta']['text'], end='', flush=True)
        # Small delay to simulate "typing" effect (optional)
        time.sleep(0.05)
    # Check for metadata in the stream
    elif "metadata" in event:
        usage_info = event['metadata']['usage']

# 5. After the stream ends, print any metadata (like token counts)
if usage_info:
    print(f"\n\n----\nToken Usage: {usage_info['inputTokens']} input tokens, {usage_info['outputTokens']} output tokens\n----\n")

print("\n\n[Stream Complete]")


