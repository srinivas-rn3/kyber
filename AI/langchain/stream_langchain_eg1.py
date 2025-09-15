from langchain_aws import ChatBedrock
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

prompt = PromptTemplate.from_template(
    "Write a detailed short story about a {animal} who becomes friends with a robot. Make it fun and imaginative."
    )

# Claude 3 Haiku model on Bedrock (ap-south-1)
llm = ChatBedrock(
    model_id = "anthropic.claude-3-haiku-20240307-v1:0",
    streaming = True,
    region_name = "ap-south-1",
    callbacks = [StreamingStdOutCallbackHandler()],
    model_kwargs = {
        "temperature": 0.6,
        "max_tokens": 200
    }
)
chain = prompt | llm | StrOutputParser()

# Stream the output token by token
chain.invoke({'animal':'cat'})
