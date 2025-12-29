import json
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

def invoke_bedrock_model():
    """
    Invoke OpenAI model via AWS Bedrock with proper error handling
    """
    try:
        # Initialize Bedrock client
        bedrock = boto3.client(
            service_name="bedrock-runtime",
            region_name="ap-south-1"
        )

        MODEL_ID = "openai.gpt-oss-20b-1:0"  # OpenAI model as requested

        # Request body for OpenAI model format
        body = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Explain RAG vs CAG in simple terms."
                        }
                    ]
                }
            ],
            "max_tokens": 500,
            "temperature": 0.3,
            "reasoning_effort": "low"  # OpenAI specific parameter
        }

        # Invoke the model
        response = bedrock.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        # Parse response
        response_body = json.loads(response["body"].read())
        
        # Extract content using OpenAI response format
        content = response_body["choices"][0]["message"]["content"]
        return content

    except NoCredentialsError:
        return "Error: AWS credentials not found. Please configure your AWS credentials."
    except ClientError as e:
        return f"AWS Client Error: {e.response['Error']['Message']}"
    except KeyError as e:
        return f"Response parsing error: Missing key {e}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

if __name__ == "__main__":
    result = invoke_bedrock_model()
    print(result)
