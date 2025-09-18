from react_agent import react_agent
from build_kb import build_kb
import config as Config
import os

def initialize_system():
    """Initialize the knowledge base if it doesn't exist"""
    # Check if vector DB directory exists and has files
    vector_db_path = Config.VECTOR_DB
    if not os.path.exists(vector_db_path) or not os.listdir(os.path.dirname(vector_db_path)):
        print("🔧 Building knowledge base for the first time...")
        try:
            # Check if source CSV exists
            if not os.path.exists(Config.KB_FILE):
                print(f"❌ Source file not found: {Config.KB_FILE}")
                return False
            
            build_kb()
            print("✅ Knowledge base built successfully!")
        except Exception as e:
            print(f"❌ Error building knowledge base: {e}")
            print("Please check your AWS credentials and network connection.")
            return False
    else:
        print("✅ Knowledge base already exists.")
    return True

if __name__ == "__main__":
    print("💰 Financial Advisor Bot Starting...")
    
    if not initialize_system():
        print("Failed to initialize system. Exiting.")
        exit(1)
    
    print("💰 Financial Advisor Bot Ready!")
    print("Ask me about your expenses, or type 'exit' to quit.")
    
    while True:
        q = input("\n💬 Your question: ")
        if q.lower() in ["exit", "quit"]:
            print("👋 Goodbye!")
            break 
        
        try:
            response = react_agent(q)
            print(f"\n🤖 Assistant: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")

