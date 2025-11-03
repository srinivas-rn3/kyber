from langchain_aws import ChatBedrock
from config.config import REGION, MODEL_ID
from memory.memory_handler import update_memory
import json, re

llm = ChatBedrock(model_id=MODEL_ID, region_name=REGION)

def classify_with_llm(state):
    """
    Uses Claude (Bedrock) to detect intent and city name.
    """

    history = state.get("history", [])
    state = update_memory(state, history)
    user_msg = state.get("message", "")

    # 🔹 Improved prompt — strictly JSON format
    prompt = f"""
    You are an intent and entity classifier.
    Analyze the user message and extract:
    - intent: one of ["weather", "alarm", "exit", "unknown"]
    - city: if user asks about weather, extract city name; else keep blank.

    You must reply with ONLY valid JSON and nothing else.

    Example 1:
    User: What's the weather in Mumbai?
    Response: {{"intent": "weather", "city": "Mumbai"}}

    Example 2:
    User: Set an alarm for 6 AM
    Response: {{"intent": "alarm", "city": ""}}

    Example 3:
    User: Exit
    Response: {{"intent": "exit", "city": ""}}

    User message: {user_msg}
    """

    response = llm.invoke(prompt)

    # 🩵 Handle both list or string responses
    if isinstance(response.content, list):
        raw_output = response.content[0].text if hasattr(response.content[0], "text") else str(response.content[0])
    else:
        raw_output = str(response.content)

    print("\n🧾 Raw LLM Output:", raw_output)

    # 🧠 Try parsing JSON
    try:
        parsed = json.loads(raw_output)
        state["intent"] = parsed.get("intent", "unknown").lower()
        state["city"] = parsed.get("city", "").strip()
    except Exception as e:
        print("⚠️ JSON parse failed:", e)
        # 🩹 Fallback regex extraction (in case Claude didn’t send pure JSON)
        match_intent = re.search(r'weather|alarm|exit', raw_output.lower())
        match_city = re.search(r'city\s*[:=]\s*([A-Za-z ]+)', raw_output)
        state["intent"] = match_intent.group(0) if match_intent else "unknown"
        state["city"] = match_city.group(1).strip() if match_city else ""

    # ✅ Move debug print here
    #print("🧾 STATE BEFORE RETURN FROM CLASSIFY:", state)
    print(f"🤖 Detected intent: {state['intent']}, City: {state['city']}")

    # ✅ Always return a full, clean state object
return {
    "message": state.get("message", ""),
    "intent": state.get("intent", "unknown"),
    "city": state.get("city", ""),
    "history": state.get("history", [])
}

