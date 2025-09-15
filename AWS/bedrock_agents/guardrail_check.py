import boto3

client = boto3.client('bedrock-runtime', region_name='ap-south-1')
model_id = 'anthropic.claude-3-haiku-20240307-v1:0'

# Your Guardrail ID from the AWS Console
guardrail_id = 'hbbdustjd1z1' 
guardrail_version = 'DRAFT'  

messages = [{
    "role": "user",
    "content": [{"text": "Hi, my email address is user@example.com. Can you help me with something?"}]
}]

try:
    # CORRECTED PARAMETER NAMES for Converse API:
    response = client.converse(
        modelId=model_id,
        messages=messages,
        guardrailConfig={
            'guardrailIdentifier': guardrail_id,  # <<< Changed from 'guardrailId'
            'guardrailVersion': guardrail_version  # <<< Correct
        }
    )
    
    answer = response['output']['message']['content'][0]['text']
    print("✅ Response:", answer)

except client.exceptions.GuardrailIntervenedException as e:
    # This exception is thrown if the Guardrail blocks the prompt or response
    print(" Guardrail Blocked the request/reason:", e.response['Error']['Message'])

except Exception as e:
    print(" Other Error:", e)