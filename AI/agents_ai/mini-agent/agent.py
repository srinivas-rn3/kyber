import json
from bedrock_client import BedrockLLM
from tools import get_weather, set_alarm, tell_joke, calculate


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
4. calculate
5. unknown

Rules:
- The user may request ONE or MULTIPLE actions in a single message.
- Return a JSON object with an "actions" key containing a list of intents.
- If user asks about weather, include an action with intent = "weather" and extract city.
- If user asks to set an alarm, include an action with intent = "set_alarm" and extract time.
- If user asks for a joke, include an action with intent = "joke".
- If user asks for arithmetic calculation, include an action with intent = "calculate" and extract expression.
- If nothing matches, return a single action with intent = "unknown".

JSON format (always return this structure):
{{"actions": [
  {{"intent": "weather", "city": "Mumbai"}},
  {{"intent": "set_alarm", "time": "6 AM"}}
]}}

Single intent example:
{{"actions": [
  {{"intent": "joke"}}
]}}

Calculation example:
{{"actions": [
  {{"intent": "calculate", "expression": "12 + 5 * 2"}}
]}}

Unknown example:
{{"actions": [
  {{"intent": "unknown"}}
]}}

User request:
{user_input}
"""

    def parse_llm_output(self, llm_output: str) -> dict:
        try:
            return json.loads(llm_output)
        except json.JSONDecodeError:
            return {"actions": [{"intent": "unknown", "raw_output": llm_output}]}

    def execute(self, user_input: str) -> str:
        prompt = self.build_router_prompt(user_input)
        llm_output = self.llm.invoke(prompt)
        print("\nRAW LLM OUTPUT:", repr(llm_output))
        decision = self.parse_llm_output(llm_output)
        print("PARSED DECISION:", decision)

        actions = decision.get("actions", [{"intent": "unknown"}])
        results = []

        for action in actions:
            print("CURRENT ACTION:", action)

            #intent = action.get("intent", "unknown")
            #print("CURRENT ACTION:", action)

            intent = action.get("intent", "unknown")
            print("CURRENT INTENT:", intent)

            if intent == "weather":
                city = action.get("city")
                if not city:
                    results.append("I understood a weather request, but no city was found.")
                else:
                    tool_result = get_weather(city)
                    print("TOOL RESULT:", tool_result)
                    results.append(tool_result)

            elif intent == "set_alarm":
                time = action.get("time")
                if not time:
                    results.append("I understood an alarm request, but no time was found.")
                else:
                    tool_result = set_alarm(time)
                    print("TOOL RESULT:", tool_result)
                    results.append(tool_result)

            elif intent == "joke":
                tool_result = tell_joke()
                print("TOOL RESULT:", tool_result)
                results.append(tool_result)
            
            elif intent == "calculate":
                expression = action.get("expression")
                if not expression:
                    results.append("I understood a calculation request, but no expression was found.")
                else:
                    tool_result = calculate(expression)
                    print("TOOL RESULT:", tool_result)
                    results.append(tool_result)

            else:
                fallback_message = f"Unsupported action returned by model: {action}"
                print("TOOL RESULT:", fallback_message)
                results.append(fallback_message)

        print("FINAL RESULTS LIST:", results)

        return "\n".join(results)
