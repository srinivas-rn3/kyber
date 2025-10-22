from langgraph.graph import END,StateGraph
from typing import TypedDict

# State: Information about user and recommendation
class State(TypedDict):
    mood: str
    recommendation: str
    genre: str

# Node 1: Analyze the mood
def analyze_mood(state:State):
    mood =  state.get("mood","").lower()
    print(f"Analyzing your mood: {mood}")

    return {
        "mood": mood,
        "recommendation": "",
        "genre": ""
    }

# Node 2: Happy mood - Comedy movies

def recommend_comedy(state:State):
    print("You're happy! Perfect time for comedy!!")

    movies = [
        "The Hangover - Hilarious adventure!",
        "Superbad - Teen comedy classic",
        "Bridesmaids - Laugh-out-loud funny",

    ]
    recommendation  = "\n".join(movies)
    return {
        "mood": state["mood"],
        "genre": "Comedy",
        "recommendation": recommendation
    }

# Node 3: Sad mood - Uplifting movies
def recommend_uplifting(state:State):
    print("You're sad! Let's cheer you up!!")

    movies = [
        "Forrest Gump - Feel-good classic",
        "Soul - Beautiful and heartwarming",
        "The Pursuit of Happyness - Uplifting film",
    ]
    recommendation  = "\n".join(movies)
    return {
        "mood": state["mood"],
        "genre": "Uplifting",
        "recommendation": recommendation
    }
# Node 4: Bored mood - Action movies
def recommend_action(state:State):
    print("You're bored! Let's get some action!!")

    movies = [
        "The Matrix - Classic sci-fi action",
        "Mad Max: Fury Road - Non-stop action",
        "John Wick - Fast-paced action",
    ]
    recommendation  = "\n".join(movies)
    return {
        "mood": state["mood"],
        "genre": "Action",
        "recommendation": recommendation
    }

# Node 5: Tired mood - Light/Easy movies
def recommend_light(state:State):
    print("You're tired! Let's get some light!!")

    movies = [
        "The Grand Budapest Hotel - Visually soothing",
        "Paddington - Gentle and charming",
        "Chef - Relaxing food movie",
    ]
    recommendation  = "\n".join(movies)
    return {
        "mood": state["mood"],
        "genre": "Light",
        "recommendation": recommendation
    }
# Decision function: Route based on mood
def route_by_mood(state:State):
    mood = state.get("mood","").lower()

    print(f"Routing based on mood: {mood}")
    if mood in ["happy", "joyful", "excited", "great", "good"]:
        return "comedy"
    elif mood in ["sad", "down", "depressed", "blue", "upset"]:
        return "uplifting"
    elif mood in ["bored", "restless", "energetic"]:
        return "action"
    elif mood in ["tired", "sleepy", "exhausted", "relaxed"]:
        return "light"
    else:
        print(" Mood not recognized, defaulting to comedy!")
        return "comedy"
# Build the graph
workflow = StateGraph(State)

# Add all nodes
workflow.add_node("analyze_mood", analyze_mood)
workflow.add_node("comedy", recommend_comedy)
workflow.add_node("uplifting", recommend_uplifting)
workflow.add_node("action", recommend_action)
workflow.add_node("light", recommend_light)

# Set starting point
workflow.set_entry_point("analyze_mood")

# Add CONDITIONAL edge - the decision maker!
workflow.add_conditional_edges(
    "analyze_mood",
    route_by_mood,{
        "comedy": "comedy",
        "uplifting": "uplifting",
        "action": "action",
        "light": "light"
    }
    
)

# Connect all recommendation nodes to END
workflow.add_edge("comedy", END)
workflow.add_edge("uplifting", END)
workflow.add_edge("action", END)
workflow.add_edge("light", END)

# Compile the app
app = workflow.compile()
# Test with different moods

print("="*70)
print("MOVIE RECOMMENDER BOT")
print("="*70)

print("\n"+"-"*60)
print("TEST1: HAPPPY MOOD")
print("\n"+"-"*60)
result1 = app.invoke({"mood": "happy"})
print(f"\n Genre: {result1['genre']}")
print(f"\n Recommendation: {result1['recommendation']}")

print("\n"+"-"*60)
print("TEST2: SAD MOOD")
print("\n"+"-"*60)
result1 = app.invoke({"mood": "Sad"})
print(f"\n Genre: {result1['genre']}")
print(f"\n Recommendation: {result1['recommendation']}")