import datetime

def lambda_handler(event, context):
    city = event.get("city", "Unknown")
    date = event.get("date", "today")

    # Convert "tomorrow" into YYYY-MM-DD
    if date.lower() == "tomorrow":
        tomorrow = datetime.date.today() + datetime.timedelta(days=1)
        date = tomorrow.strftime("%Y-%m-%d")

    # Mock data
    weather_data = {
        "Bangalore": {"2025-09-06": "27°C, light rain"},
        "Mumbai": {"2025-09-06": "30°C, humid with clouds"}
    }

    forecast = weather_data.get(city, {}).get(date, "Weather data not available")

    # ✅ Correct response format for Bedrock Agent
    return {
        "response": {
            "content": [
                {
                    "text": f"The weather in {city} on {date} is {forecast}."
                }
            ]
        }
    }
