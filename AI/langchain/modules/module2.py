from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
import boto3

# 1. Setup the AI model (simple)
chat = ChatBedrock(
    client=boto3.client("bedrock-runtime", "ap-south-1"),
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_kwargs={"temperature": 0.7, "max_tokens": 200}
)

# 2. Setup memory (only for current session)
memory = ConversationBufferMemory(
    memory_key='chat_history',
    return_messages=True
)

# 3. Simple prompt template
template = """You provide 3 interesting facts about topics.

Current conversation:
{chat_history}

User: {human_input}
AI: Provide 3 facts:"""

prompt = ChatPromptTemplate.from_template(template)

# 4. Create the chain
fact_finder = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=False
)

# 5. Simple interaction (no file saving, no complex stuff)
print("🌟 Simple Fact Finder (Type 'quit' to exit)")
print("Note: I'll only remember during this session")

while True:
    user_input = input("\nWhat topic? ").strip()
    
    if user_input.lower() == "quit":
        break
        
    # Get and show facts
    response = fact_finder.invoke({'human_input': user_input})
    print(f"\n📚 Facts about {user_input.title()}:")
    print(response['text'])
    print("-" * 50)

print("✅ Session ended - Thanks for using!")