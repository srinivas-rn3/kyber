from langchain_aws import ChatBedrock
from config.config import *
import json

llm =  ChatBedrock(model_id=MODEL_ID,region_name=REGION_NAME)

def classify_with_llM(state):
    user_msg = state.get("message","")

    prompt = f"""
    You are a travel flight assistant intent classifier.
    Extract structured info from the user message.

    Identify:
    1. intent: one of ["check_flight", "book_flight", "cancel_flight", "exit", "unknown"]
    2. destination: flight destination city if mentioned
    3. date: if user mentions day or date ("tomorrow", "Friday", "12th Jan")
    4. time: if user specifies morning/evening/time
    5. airline: if mentioned (optional)

    Respond strictly as JSON.

    Example 1:
    User: "When is my next flight to Singapore?"
    → {{"intent": "check_flight", "destination": "Singapore", "date": "next flight", "time": "", "airline": ""}}

    Example 2:
    User: "Book a flight to Paris on Friday morning"
    → {{"intent": "book_flight", "destination": "Paris", "date": "Friday", "time": "morning", "airline": ""}}

    Example 3:
    User: "Cancel my Emirates flight to Dubai"
    → {{"intent": "cancel_flight", "destination": "Dubai", "date": "", "time": "", "airline": "Emirates"}}

    User message: {user_msg}
    """
    response = llm.invoke(prompt)
    raw_output = response.content[0].text if isinstance(response.content, list) else (response.content)

    try:
        parsed = json.loads(raw_output)
        for key in ['intent','destination', 'date', 'time', 'airline']:
            state[key] = parsed.get(key, "")
    except Exception as e:
        print("⚠️ Parse failed:", e, "\nRaw:", raw_output)
        state.update({"intent": "unknown", "destination": "", "date": "", "time": "", "airline": ""})
    
    print(f"intent={state['intent']},dest={state['destination']},date={state['date']},time={state['time']},airline={state['airline']}")
    return state


