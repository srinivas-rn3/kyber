from research_assistant import SimpleResearchAssistant

# Configuration
SHOW_SOURCES = True

def main():
    print("🤖 AWS Research Assistant - Simple Version")
    print("=" * 50)

    # Create Assistant 
    assistant = SimpleResearchAssistant("demo-session-001")

    # Load documents (if any)
    assistant.load_documents()

    # Demo questions
    questions = [
        "What are the main topics in these documents?",
        "Can you summarize the key points?",
        "What sources did you use for this information?"
    ]
    print("\nStarting conversation...")
    print("=" * 50)
    
    for i,question in enumerate(questions,1):
        print(f"\n{i}.You:{question}")

        response = assistant.ask(question)

        print(f"\nAssistant: {response['answer']}")

        if SHOW_SOURCES and response['sources']:
            print(f"Sources: {', '.join(response['sources'])}")
        
        # Session info (assuming this method exists)
        info = assistant.get_session_info()
        print(f"\n📊 Session Info: {info['questions_asked']} questions asked using {info['model']}")

if __name__ == '__main__':
    main()
    