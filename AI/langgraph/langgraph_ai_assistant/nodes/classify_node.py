from langchain_aws import ChatBedrock
from config.config import REGION, MODEL_ID
from memory.memory_handler import update_memory
import json

# ----------------------------------------
# 🔧 Initialize the Bedrock Claude model
# ----------------------------------------
llm = ChatBedrock(model_id=MODEL_ID, region_name=REGION)

# ----------------------------------------
# 🧠 Node: classify_with_llm
# ----------------------------------------
def classify_with_llm(state):
    """
    This node uses Claude (via Bedrock) to analyze user input
    and extract both the intent (weather, alarm, exit, unknown)
    and the city name (if weather-related).
    """

    # 1️⃣ Update memory (store latest message in conversation history)
    history = state.get("history", [])
    state = update_memory(state, history)

    # 2️⃣ Read the user's message
    user_msg = state.get("message", "")

    # 3️⃣ Build an LLM prompt
    prompt = f"""
    You are an intent and entity classifier.
    From the user's message, extract:
    1. intent: one of ["weather", "alarm", "exit", "unknown"]
    2. city: if the message asks about weather, extract the city name.
       If no city is mentioned, leave it blank.

    Return output strictly as JSON, like this:
    {{"intent": "weather", "city": "Bangalore"}}

    Example 1:
    User: "What's the weather in Mumbai?"
    Response: {{"intent": "weather", "city": "Mumbai"}}

    Example 2:
    User: "Set an alarm for 6 AM"
    Response: {{"intent": "alarm", "city": ""}}

    Example 3:
    User: "Exit"
    Response: {{"intent": "exit", "city": ""}}

    User message: {user_msg}
    """

    # 4️⃣ Invoke Claude via Bedrock
    response = llm.invoke(prompt)

    # 5️⃣ Handle both string and list responses safely
    if isinstance(response.content, list):
        intent_text = response.content[0].text if hasattr(response.content[0], "text") else str(response.content[0])
    else:
        intent_text = str(response.content)

    # 6️⃣ Try parsing the LLM output as JSON
    try:
        parsed = json.loads(intent_text)
        state["intent"] = parsed.get("intent", "unknown").lower()
        state["city"] = parsed.get("city", "")
    except Exception as e:
        print("⚠️ Failed to parse LLM response as JSON:", e)
        print("Raw response was:", intent_text)
        state["intent"] = "unknown"
        state["city"] = ""

    # 7️⃣ Log what the model detected
    print(f"🤖 Detected intent: {state['intent']}, City: {state['city']}")

    # 8️⃣ Return updated state for next node
    return state
