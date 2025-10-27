# test_all.py
from research_assistant import SimpleResearchAssistant

# Test initialization
assistant = SimpleResearchAssistant("test-session")
print("✅ Research Assistant created successfully!")

# Test memory
history = assistant.memory.get_history()
print(f"✅ Memory works! History length: {len(history)}")

# Test vector store
docs = assistant.vector_store.search("test")
print(f"✅ Vector store works! Found {len(docs)} docs")

print("🎉 All systems go!")