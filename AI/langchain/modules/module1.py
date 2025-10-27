import json
from datetime import datetime
from langchain_aws import ChatBedrock
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_core.messages import HumanMessage, AIMessage
import boto3
import os

# Configuration
MEMORY_FILE = r"C:\Users\srini\OneDrive\kiro\kyber\AI\langchain\modules\logs_mem\fact_finder_memory.json"
os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)

# Custom memory loader/saver
def load_memory():
    """Load conversation history from file"""
    try:
        with open(MEMORY_FILE, 'r') as f:
            data = json.load(f)
            memory = ConversationBufferMemory(
                memory_key='chat_history',
                return_messages=True,
                input_key='human_input'
            )
            # Reconstruct message objects
            memory.chat_memory.messages = [
                HumanMessage(content=msg['content']) if msg['type'] == 'human' 
                else AIMessage(content=msg['content'])
                for msg in data['history']
            ]
            return memory, data.get('stats', {})
    except (FileNotFoundError, json.JSONDecodeError):
        return ConversationBufferMemory(
            memory_key='chat_history',
            return_messages=True,
            input_key='human_input'
        ), {'topics': {}, 'total_queries': 0}

def save_memory(memory, stats):
    """Save conversation history to file"""
    with open(MEMORY_FILE, 'w') as f:
        json.dump({
            'history': [
                {
                    'type': 'human' if isinstance(msg, HumanMessage) else 'ai',
                    'content': msg.content,
                    'timestamp': str(datetime.now())
                }
                for msg in memory.buffer
            ],
            'stats': stats
        }, f, indent=2)

# Initialize components
memory, stats = load_memory()
stats.setdefault('topics', {})
stats.setdefault('total_queries', 0)

chat = ChatBedrock(
    client=boto3.client("bedrock-runtime", "ap-south-1"),
    model_id="anthropic.claude-3-haiku-20240307-v1:0",
    model_kwargs={"temperature": 0.7, "max_tokens": 256}
)

template = """You are a helpful fact bot that provides exactly 3 unique facts about any topic.

Guidelines:
- Provide exactly 3 facts
- Make facts distinct and interesting
- For repeated topics, provide new facts
- Keep responses concise

Conversation history:
{chat_history}

New request: {human_input}

3 facts:"""
prompt = ChatPromptTemplate.from_template(template)

fact_finder = LLMChain(
    llm=chat,
    prompt=prompt,
    memory=memory,
    verbose=False
)

# Main interaction loop
print("\n★ Fact Finder 2.0 ★ (Type 'quit' to exit, 'stats' for usage)")
while True:
    try:
        user_input = input("\nWhat topic would you like facts about? ").strip()
        
        if not user_input:
            continue
            
        if user_input.lower() == "quit":
            break
            
        if user_input.lower() == "stats":
            print(f"\n📊 Usage Statistics:")
            print(f"Total queries: {stats['total_queries']}")
            print("Top topics:")
            for topic, count in sorted(stats['topics'].items(), key=lambda x: -x[1])[:5]:
                print(f"- {topic.title()}: {count} times")
            continue
            
        # Update statistics
        stats['total_queries'] += 1
        stats['topics'][user_input.lower()] = stats['topics'].get(user_input.lower(), 0) + 1
        
        # Get facts
        response = fact_finder.invoke({'human_input': user_input})
        
        # Display results
        print(f"\n🔍 Facts about {user_input.title()}:")
        print(response['text'])
        
    except KeyboardInterrupt:
        break
    except Exception as e:
        print(f"⚠️ Error: {e}")

# Save before exiting
save_memory(memory, stats)
print(f"\n💾 Conversation history saved to {MEMORY_FILE}")
print("👋 Goodbye!")