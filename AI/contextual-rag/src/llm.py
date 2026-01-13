from langchain_aws import ChatBedrock
from langchain_aws.embeddings import BedrockEmbeddings

llm = ChatBedrock(
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    region_name="ap-south-1",
    temperature=0.2
)

embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v2:0",
    region_name="ap-south-1"
)
