from research_assistant import SimpleResearchAssistant
from config import *

def interactive_chat():
    print("🤖 AWS Research Assistant - Interactive Chat")
    print("Type 'quit' to exit, 'info' for session info")
    print("=" * 50)
    
    session_id = input("Enter session name (or press Enter for 'main'): ").strip()
    if not session_id:
        session_id = "main-session"
    
    # Create assistant
    assistant = SimpleResearchAssistant(session_id)
    
    # Load documents
    print("Loading documents...")
    assistant.load_documents()
    
    print("\nReady! Ask me anything about your documents.")
    print("=" * 50)
    
    while True:
        question = input("\n🧑‍💻 You: ").strip()
        
        if question.lower() == 'quit':
            break
        elif question.lower() == 'info':
            info = assistant.get_session_info()
            print(f"📊 Session: {info['session_id']}, Questions: {info['questions_asked']}")
            continue
        elif not question:
            continue
        
        print("🤖 Thinking...")
        response = assistant.ask(question)
        
        print(f"\n🤖 Assistant: {response['answer']}")
        
        if SHOW_SOURCES and response['sources']:
            print(f"📚 Sources: {', '.join(response['sources'])}")
    
    print("👋 Goodbye!")

if __name__ == "__main__":
    interactive_chat()