from langgraph.graph  import StateGraph,END
from typing import TypedDict

# State: What information flows through the bot
class State(TypedDict):
    temperature: int
    advice: str
    weather_type : str

# Node 1: Analyze the temperature
def analyze_weather(state: State):
    temp = state['temperature']
    print(f"Checking the temperature: {temp} °C")

    #determine weater type
    if temp > 30:
        weather_type = 'hot'
    elif temp < 15:
        weather_type = 'cold'
    else:
        weather_type = 'moderate'
    
    return {
        "temperature": temp,
        "weather_type": weather_type,
        "advice": ""
    }


# Node 2: Hot weather advice
def hot_weather_advice(state: State):
    print("Its Hot outside!!!")
    advice =  "Stay hydrated and avoid staying in the sun too long!.Use sunscreen and wear light clothes"
    return {
        "temperature": state['temperature'],
        "weather_type": state['weather_type'],
        "advice": advice
    }

# Node 3: Cold weather advice
def cold_weather_advice(state: State):
    print("Its Cold outside!!!")
    advice = "Wear warm clothes! Dont forget your scarf and gloves.Stay Warm!"
    return {
        "temperature": state['temperature'],
        "weather_type": state['weather_type'],
        "advice": advice
    }

# Node 4: Moderate weather advice
def moderate_weather_advice(state: State):
    print("Its Moderate outside!!!")
    advice = "Enjoy the weather! Wear light clothes and bring a light jacket."
    return {
        "temperature": state['temperature'],
        "weather_type": state['weather_type'],
        "advice": advice
    }

# Decision function: Routes to different advice based on weather
def route_by_weather(state: State):
    weather =  state['weather_type']
    print(f"Weather type detected:{weather}")
    return weather

# Build the graph
workflow = StateGraph(State)

# Add all nodes
workflow.add_node("analyze",analyze_weather)
workflow.add_node("hot_advice", hot_weather_advice)
workflow.add_node("cold_advice", cold_weather_advice)
workflow.add_node("moderate_advice", moderate_weather_advice)

# Set starting point
workflow.set_entry_point("analyze")

# Add CONDITIONAL edge - this is the decision maker!
workflow.add_conditional_edges(
    "analyze",
    route_by_weather,
    {
    "hot":"hot_advice",
    "cold":"cold_advice",
    "moderate":"moderate_advice",
    }
)

# Connect all advice nodes to END
workflow.add_edge("hot_advice",END)
workflow.add_edge("cold_advice", END)
workflow.add_edge("moderate_advice", END)


# Compile the app
app = workflow.compile()

# Test with different temperatures
print("="*50)
#print("TEST 1: HotDay")
print("="*50)
result1 = app.invoke({"temperature": 5,"weather_type": "","advice" : ""})
print(f"Advice :{result1['advice']}")

print("="*50)
#print("TEST 2: ColdDay")
print("="*50)
result2 = app.invoke({"temperature": 110, "weather_type": "", "advice" : ""})
print(f"Advice :{result2['advice']}")

print("="*50)
#print("TEST 3: ModerateDay")
print("="*50)
result3 = app.invoke({"temperature": 20, "weather_type": "", "advice" : ""})
print(f"Advice :{result3['advice']}")
