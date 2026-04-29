def get_weather(city: str) -> str:
    """Return mock weather information for a given city."""
    weather_data = {
        "bangalore": "Cloudy, 27°C",
        "mumbai": "Rainy, 30°C",
        "delhi": "Sunny, 35°C",
        "hyderabad": "Hot, 33°C",
    }
    result = weather_data.get(city.lower())
    if result:
        return f"Weather in {city}: {result}"
    return f"No weather data found for {city}."


def set_alarm(time: str) -> str:
    """Return a confirmation message for setting an alarm."""
    return f"Alarm set successfully for {time}"

def tell_joke() -> str:
    """Return a simple programmer joke."""
    return "Why do programmers prefer dark mode? Because light attracts bugs."