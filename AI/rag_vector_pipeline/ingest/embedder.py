from langchain_aws import BedrockEmbeddings
from config.bedrock_config import get_bedrock_client

def get_titan_embeddings():
    client = get_bedrock_client()
    return BedrockEmbeddings(
        model_id="amazon.titan-embed-text-v2:0",
        client=client
    )
