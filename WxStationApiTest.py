#weather station test pi pico W api

import requests
from datetime import datetime

def get_temperature_and_humidity():
    url = "http://<yourpipicoip>/data"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            temperature = data['temperature']
            humidity = data['humidity']
            return temperature, humidity
        else:
            print("Failed to get data from the server")
            return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

temperature, humidity = get_temperature_and_humidity()
if temperature is not None and humidity is not None:
    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    weather_response_prompt = f"[OOC: The weather station reported back to you the current household temperature and humidity. The data report is: {temperature}°C and {humidity}% as of {current_datetime}. Report your findings to the user.]"
else:
    weather_response_prompt = "[OOC: Unable to retrieve the weather data at this time.]"

print(weather_response_prompt)
