import boto3
import json

#  Bedrock runtime client (Mumbai region)
bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')
MODEL_ID = "anthropic.claude-3-haiku-20240307-v1:0"

def call_claude(prompt: str) -> str:
    """Call Claude 3 Haiku using AWS Bedrock."""

    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 500,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = bedrock.invoke_model (modelId=MODEL_ID,body=json.dumps(body))

    result = json.loads(response['body'].read())
   
    return result['content'][0]['text']
