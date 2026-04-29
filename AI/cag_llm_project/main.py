import json
import boto3
import os

bedrock = boto3.client('bedrock-runtime', region_name='ap-south-1')

# Use relative paths
script_dir = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(script_dir, 'rules.json')) as f:
    rules = json.load(f)
with open(os.path.join(script_dir, 'customer.json')) as f:
    customer = json.load(f)

prompt = f"""
You are a strict insurance policy engine. Follow rules exactly.

BUSINESS RULES:
- Max expiry days allowed: {rules['max_expiry_days']}
- Allowed statuses: {rules['allowed_status']}

CUSTOMER:
- Status: {customer['status']}
- Days expired: {customer['days_expired']}

QUESTION:
Can I renew my policy?

RULE:
If days expired > max allowed → ALWAYS answer NOT ELIGIBLE.
"""
# ---- FIXED PAYLOAD ----
payload = {
    "anthropic_version": "bedrock-2023-05-31",
    "max_tokens": 300,  # Correct parameter for Claude 3 models
    "messages": [
        {
            "role": "user",
            "content": prompt
        }
    ]
}

response = bedrock.invoke_model(
    modelId='anthropic.claude-3-haiku-20240307-v1:0',
    body=json.dumps(payload)
)


data = json.loads(response['body'].read())
print("\nLLM ANSWER (CAG):\n")
print(data['content'][0]['text'])
