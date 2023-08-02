# weather.py
import requests
import os
from datetime import date
from gtts import gTTS




def get_weather(api_key):
    city_name = input("Enter City: ")
    base_url = "http://api.weatherapi.com/v1/forecast.json"
    params = {
        "key": api_key,
        "q": city_name,
        "days": 3,  # Number of days of forecast data (max 3 for free plan)
        "aqi": "no"  # Disable air quality data if not needed
    }

    response = requests.get(base_url, params=params)
    data = response.json()

    if "error" not in data:
        location = data["location"]["name"]

        # Current weather data
        current_weather = data["current"]["condition"]["text"]
        current_temperature = data["current"]["temp_c"]
        current_humidity = data["current"]["humidity"]
        current_wind_speed = data["current"]["wind_kph"]

        print(f"Weather in {location} (Current): {current_weather}")
        print(f"Temperature: {current_temperature}°C")
        print(f"Humidity: {current_humidity}%")
        print(f"Wind Speed: {current_wind_speed} km/h")

        # Extract today's forecast
        today = date.today().isoformat()
        forecast_data = data["forecast"]["forecastday"]
        today_forecast = next((day for day in forecast_data if day["date"] == today), None)

        if today_forecast:
            forecast_weather = today_forecast["day"]["condition"]["text"]
            max_temperature = today_forecast["day"]["maxtemp_c"]
            min_temperature = today_forecast["day"]["mintemp_c"]

            print(f"Weather in {location} (Forecast for {today}): {forecast_weather}")
            print(f"Max Temperature: {max_temperature}°C")
            print(f"Min Temperature: {min_temperature}°C")

            # Convert weather information to speech
            text_to_speak = (
                "Hi Jeason"
                f"Current weather in {location} is {current_weather}. "
                f"The temperature is {current_temperature} degrees Celsius. "
                f"The humidity is {current_humidity}%. "
                f"The wind speed is {current_wind_speed} kilometers per hour. "
                f"Today's weather is forecasted to be {forecast_weather}. "
                f"The maximum temperature will be {max_temperature} degrees Celsius, "
                f"and the minimum temperature will be {min_temperature} degrees Celsius."
            )

            # Create a gTTS object and save it to a temporary file
            tts = gTTS(text=text_to_speak, lang="en", slow=False)
            tts.save("weather.mp3")

            # Play the speech using afplay on macOS
            os.system("afplay -r 1.5 weather.mp3")
        else:
            print("Today's weather forecast not available.")
    else:
        print(f"Failed to fetch weather data. Error: {data['error']['message']}")