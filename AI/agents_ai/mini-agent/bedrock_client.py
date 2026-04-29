import json
import boto3
from config import AWS_REGION, MODEL_ID, MAX_TOKENS, TEMPERATURE


class BedrockLLM:
    def __init__(self):
        self.client = boto3.client("bedrock-runtime", region_name=AWS_REGION)
        self.model_id = MODEL_ID

    def invoke(self, prompt: str) -> str:
        request_body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

        response = self.client.invoke_model(
            modelId=self.model_id,
            body=json.dumps(request_body),
            contentType="application/json",
            accept="application/json"
        )

        response_body = json.loads(response["body"].read())
        return response_body["content"][0]["text"]
