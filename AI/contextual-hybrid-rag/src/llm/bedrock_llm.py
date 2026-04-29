import boto3
import json

class BedrockLLM:
    def __init__(self,region="ap-south-1"):
        self.client = boto3.client("bedrock-runtime", region_name=region)

        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    
    def invoke(self,prompt:str) -> str:

        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 120,
            "temperature": 0,
            "messages": [{"role": "user", "content": prompt}]
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(body)
        )

        result =  json.loads(response['body'].read())
        return result['content'][0]['text'].strip()