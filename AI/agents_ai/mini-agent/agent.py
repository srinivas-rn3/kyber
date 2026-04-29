import json
from bedrock_client import BedrockLLM
from tools import get_weather, set_alarm, tell_joke


class MiniAgent:
    def __init__(self):
        self.llm = BedrockLLM()

    def build_router_prompt(self, user_input: str) -> str:
        return f"""
You are an AI routing agent.

Your job is to read the user request and return ONLY valid JSON.
Do not explain anything.
Do not add markdown.
Do not add extra text.

Available intents:
1. weather
2. set_alarm
3. joke
4. unknown

Rules:
- If user asks about weather, return intent = "weather" and extract city.
- If user asks to set an alarm, return intent = "set_alarm" and extract time.
- If user asks for a joke, return intent = "joke".
- If request does not match, return intent = "unknown".

JSON formats:

For weather:
{{"intent": "weather", "city": "Bangalore"}}

For set_alarm:
{{"intent": "set_alarm", "time": "7 AM"}}

For joke:
{{"intent": "joke"}}

For unknown:
{{"intent": "unknown"}}

User request:
{user_input}
"""

    def parse_llm_output(self, llm_output: str) -> dict:
        try:
            return json.loads(llm_output)
        except json.JSONDecodeError:
            return {"intent": "unknown", "raw_output": llm_output}

    def execute(self, user_input: str) -> str:
        prompt = self.build_router_prompt(user_input)
        llm_output = self.llm.invoke(prompt)
        decision = self.parse_llm_output(llm_output)

        intent = decision.get("intent", "unknown")

        if intent == "weather":
            city = decision.get("city")
            if not city:
                return "I understood this as a weather request, but no city was found."
            return get_weather(city)

        if intent == "set_alarm":
            time = decision.get("time")
            if not time:
                return "I understood this as an alarm request, but no time was found."
            return set_alarm(time)

        if intent == "joke":
            return tell_joke()

        return "Sorry, I could not understand the request."