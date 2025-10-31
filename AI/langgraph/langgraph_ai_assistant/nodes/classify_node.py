from langchain_aws import ChatBedrock
from config.config import REGION, MODEL_ID
from memory.memory_handler import update_memory

llm = ChatBedrock(model_id=MODEL_ID, region_name=REGION)

def classify_with_llm(state):
    # 🧠 Update memory before calling the LLM
    history = state.get("history", [])
    state = update_memory(state, history)

    user_msg = state["message"]

    prompt = f"""
    You are an intent classifier.
    Here is the chat history (most recent first):
    {state['history']}

    Based on the user's last message, return one of:
    - weather
    - alarm
    - exit
    - unknown

    Respond with only the intent word.

    User: {user_msg}
    """

    response = llm.invoke(prompt)

    # 🩹 Fix: Handle both string and structured outputs
    if isinstance(response.content, list):
        intent_text = response.content[0].text if hasattr(response.content[0], "text") else str(response.content[0])
    else:
        intent_text = str(response.content)

    intent = intent_text.strip().lower()

    if intent not in ["weather", "alarm", "exit"]:
        intent = "unknown"

    print(f"🤖 Detected intent: {intent}")
    state["intent"] = intent
    return state
