import boto3
import datetime
import uuid

from langchain.memory import ConversationBufferMemory
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, AIMessage
from boto3.dynamodb.conditions import Key



# -------------------------
# AWS + DynamoDB Setup
# -------------------------

dynamo = boto3.resource('dynamodb',region_name='ap-south-1')
table = dynamo.Table('ChatMemory')

def save_message(user_id:str,role:str,content:str):
    ts = datetime.datetime.now().isoformat()
    sk = f"MSG#{uuid.uuid4().hex[:8]}"
    item = {
        "pk":f"{user_id}",
        "sk":sk,
        "role":role,
        "content":content,
        "created_at":ts
    }
    table.put_item(Item=item)

def fetch_message(user_id:str,limit=20):
    response = table.query(
        KeyConditionExpression = Key("pk").eq(f"{user_id}"),
        ScanIndexForward=False,
        Limit=limit        
    )
    return response['Items']


def restore_memory_from_db(user_id:str, memory:ConversationBufferMemory,limit=20):
    """Replay DynamoDB messages into LangChain memory"""
    msgs = fetch_message(user_id,limit=limit)
    # Sort messages by timestamp to ensure correct order
    sorted_msgs = sorted(msgs, key=lambda x: x['created_at'])
    
    for m in sorted_msgs:
        if m["role"] == "user":
            memory.chat_memory.add_user_message(m["content"])
        else:
            memory.chat_memory.add_ai_message(m["content"])
    
# -------------------------
# Memory + LLM Setup
# -------------------------
llm = ChatBedrock(model_id = "anthropic.claude-3-haiku-20240307-v1:0",region_name="ap-south-1")
memory = ConversationBufferMemory(memory_key='chat_history',return_messages=True)

# -------------------------
# Chat Simulation
# -------------------------
user_id = 'u1'
user_msg = "My name is Srinivas"
save_message(user_id,"user",user_msg)

# AI responds
ai_msg = "Nice to meet you Srinivas!"
save_message(user_id,"ai",ai_msg)
print("AI :" ,ai_msg)

# Later: recall from memory (create fresh memory instance)
memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
restore_memory_from_db(user_id,memory)


print("\n - DynamoDb fetched history:")
for m in fetch_message(user_id):
    print(m['role'],':',m['content'])

print("\n* Restored LangChain Memory:")
print(memory.load_memory_variables({}))

# 4. Ask again
new_user_msg = "What’s my name?"
save_message(user_id, "user", new_user_msg)
# Don't add to memory yet - we'll do it after getting the response

# Get conversation history and create proper message list
chat_history = memory.load_memory_variables({})["chat_history"]
messages = chat_history + [HumanMessage(content=new_user_msg)]

# Ensure the conversation starts with a user message (Claude requirement)
if messages and isinstance(messages[0], AIMessage):
    # Remove leading AI messages to ensure user message comes first
    while messages and isinstance(messages[0], AIMessage):
        messages.pop(0)

response = llm.invoke(messages)
ai_response = response.content
print("\nAI:", ai_response)

# Save AI response to both DB and memory
save_message(user_id, "ai", ai_response)
memory.chat_memory.add_user_message(new_user_msg)  # Add user message now
memory.chat_memory.add_ai_message(ai_response)





