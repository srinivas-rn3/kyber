import requests
from config.config import *

def weather_api_node(state):
    """
    This node uses OpenWeatherMap API to get real weather info.
    It expects a city name in state["city"].
    """
    #print("🧾 STATE RECEIVED IN WEATHER NODE:", state)
    city = state.get("city", "").strip() or "Bangalore"

    print(f"Fetching real-time weather info for : {city}")

    url = f"{OPENWEATHER_API_URL}{city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        if data.get("cod") != 200:
            print(f"⚠️ Couldn't find weather for {city}. API response: {data.get('message', 'Unknown error')}")
            state['weather_result'] = f"No data found for {city}"
            return state
        
        main = data["weather"][0]["main"]
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        feels_like = data["main"]["feels_like"]

        weather_info = f"{city}: {main} ({description}), {temp}°C (feels like {feels_like}°C), humidity {humidity}%"
        print(f"✅ {weather_info}")

        state["weather_result"] = weather_info
    
    except Exception as e:
        print("❌ Error fetching weather:", e)
        state['weather_result'] = f"Weather API Error"
    
    return state