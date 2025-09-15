import json

def lambda_handler(event, context):
    # TODO implement
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
import json
import urllib.request
import boto3
from botocore.exceptions import ClientError

secretsmanager = boto3.client('secretsmanager')

def get_secret(secret_name):
    """
    Retrieves the secret from AWS Secrets Manager.
    """
    try:
        get_secret_value_response = secretsmanager.get_secret_value(SecretId=secret_name)
        print("Secret retrieved successfully")
    except ClientError as e:
        raise e
    secret = get_secret_value_response['SecretString']
    return json.loads(secret)

def lambda_handler(event, context):
    print("Received full event: " + json.dumps(event)) # This log is crucial for debugging
    
    # --- Step 1: Extract parameters from the Bedrock Agent event ---
    # The parameters are nested in the event structure
    try:
        # The input parameters are in event['parameters']
        parameters = event.get('parameters', [])
        input_parameters = {}
        
        # Convert the list of parameters into a simple dictionary
        for param in parameters:
            input_parameters[param['name']] = param['value']
            
        symbol = input_parameters.get('symbol')
        print(f"Extracted symbol: {symbol}")
        
    except Exception as e:
        print(f"Error parsing input parameters: {e}")
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event['actionGroup'],
                'apiPath': event['apiPath'],
                'httpMethod': event['httpMethod'],
                'httpStatusCode': 400,
                'responseBody': {
                    'application/json': {
                        'body': "Error: Failed to parse input parameters from the agent."
                    }
                }
            }
        }
    
    if not symbol:
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event['actionGroup'],
                'apiPath': event['apiPath'],
                'httpMethod': event['httpMethod'],
                'httpStatusCode': 400,
                'responseBody': {
                    'application/json': {
                        'body': "Error: No stock symbol provided in the request."
                    }
                }
            }
        }
    
    # --- Step 2: Retrieve the API Key from Secrets Manager ---
    secret_name = "bedrock/agents/stockpriceapi1"
    try:
        secret = get_secret(secret_name)
        api_key = secret['alpha_vantage_api_key']
    except Exception as e:
        print(f"Error retrieving API key from Secrets Manager: {e}")
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event['actionGroup'],
                'apiPath': event['apiPath'],
                'httpMethod': event['httpMethod'],
                'httpStatusCode': 500,
                'responseBody': {
                    'application/json': {
                        'body': "Error: Configuration issue. Please try again later."
                    }
                }
            }
        }
    
    # --- Step 3: Call the External API ---
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={api_key}"
    print(f"Calling URL: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
        print(f"API response: {data}")
    except Exception as e:
        print(f"Error calling Alpha Vantage API: {e}")
        return {
            'messageVersion': '1.0',
            'response': {
                'actionGroup': event['actionGroup'],
                'apiPath': event['apiPath'],
                'httpMethod': event['httpMethod'],
                'httpStatusCode': 500,
                'responseBody': {
                    'application/json': {
                        'body': f"Error calling stock API: {str(e)}"
                    }
                }
            }
        }
    
    # --- Step 4: Process the Response ---
    price = data.get("Global Quote", {}).get("05. price", "Price not found")
    
    # --- Step 5: Format the Response for Bedrock Agent ---
    response_body = {
        "application/json": {
            "body": f"The current price of {symbol} is ${price}."
        }
    }
    
    action_response = {
        'messageVersion': '1.0',
        'response': {
            'actionGroup': event['actionGroup'],
            'apiPath': event['apiPath'],
            'httpMethod': event['httpMethod'],
            'httpStatusCode': 200,
            'responseBody': response_body
        }
    }
    
    return action_response