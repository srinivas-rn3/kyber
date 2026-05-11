import json
from typing import TypedDict, List, Dict, Any

from langgraph.graph import StateGraph, START, END

from bedrock_client import BedrockLLM
from tools import get_weather, set_alarm, tell_joke, calculate


class AgentState(TypedDict):
    user_input: str
    prompt: str
    llm_output: str
    actions: List[Dict[str, Any]]
    results: List[str]
    final_response: str


def build_router_prompt(user_input: str) -> str:
    return f"""
You are an AI routing agent.

Your job is to read the user request and return ONLY valid JSON.
Do not explain anything.
Do not add markdown.
Do not add code fences.
Do not add extra text before or after JSON.

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

JSON format:
{{"actions": [
  {{"intent": "weather", "city": "Mumbai"}},
  {{"intent": "set_alarm", "time": "6 AM"}}
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


def parse_llm_output(llm_output: str) -> Dict[str, Any]:
    cleaned = llm_output.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned.removeprefix("```json").strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```").strip()
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    try:
        parsed = json.loads(cleaned)

        if "intent" in parsed and "actions" not in parsed:
            return {"actions": [parsed]}

        if "actions" in parsed and isinstance(parsed["actions"], list):
            return parsed

        return {"actions": [{"intent": "unknown"}], "raw_output": llm_output}

    except json.JSONDecodeError:
        return {"actions": [{"intent": "unknown"}], "raw_output": llm_output}


def build_graph():
    # Instantiate here so MODEL_ID env var is already set by app.py before import
    llm = BedrockLLM()

    def route_request(state: AgentState) -> AgentState:
        prompt = build_router_prompt(state["user_input"])
        llm_output = llm.invoke(prompt)

        print("\nRAW LLM OUTPUT:", repr(llm_output))

        parsed = parse_llm_output(llm_output)
        actions = parsed.get("actions", [{"intent": "unknown"}])

        print("PARSED ACTIONS:", actions)

        return {
            **state,
            "prompt": prompt,
            "llm_output": llm_output,
            "actions": actions,
        }

    def execute_actions(state: AgentState) -> AgentState:
        results = []

        for action in state["actions"]:
            print("CURRENT ACTION:", action)

            intent = action.get("intent", "unknown")
            print("CURRENT INTENT:", intent)

            if intent == "weather":
                city = action.get("city")
                if not city:
                    tool_result = "I understood a weather request, but no city was found."
                else:
                    tool_result = get_weather(city)

            elif intent == "set_alarm":
                time = action.get("time")
                if not time:
                    tool_result = "I understood an alarm request, but no time was found."
                else:
                    tool_result = set_alarm(time)

            elif intent == "joke":
                tool_result = tell_joke()

            elif intent == "calculate":
                expression = action.get("expression")
                if not expression:
                    tool_result = "I understood a calculation request, but no expression was found."
                else:
                    tool_result = calculate(expression)

            else:
                tool_result = f"Unsupported action returned by model: {action}"

            print("TOOL RESULT:", tool_result)
            results.append(tool_result)

        return {
            **state,
            "results": results,
        }

    def format_response(state: AgentState) -> AgentState:
        final_response = "\n".join(state["results"])
        print("FINAL RESULTS LIST:", state["results"])

        return {
            **state,
            "final_response": final_response,
        }

    graph = StateGraph(AgentState)

    graph.add_node("route_request", route_request)
    graph.add_node("execute_actions", execute_actions)
    graph.add_node("format_response", format_response)

    graph.add_edge(START, "route_request")
    graph.add_edge("route_request", "execute_actions")
    graph.add_edge("execute_actions", "format_response")
    graph.add_edge("format_response", END)

    return graph.compile()
