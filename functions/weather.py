import requests
from datetime import datetime, timedelta

def get_temperature(city: str):
    API_KEY = '4da963f52f6d90f3456286d7c91b681b'

    # The base URL for the OpenWeatherMap API (current weather data endpoint)
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    # Complete URL
    URL = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"

    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json() 
        
        main_data = data['main']
        temperature = main_data['temp']
        
        # Convert to Kelvin
        return round(temperature + 273.15, 2)
    
    else:
        return None
    


def get_temperature_delta_from_Milan(city: str):
    API_KEY = '4da963f52f6d90f3456286d7c91b681b'

    # The base URL for the OpenWeatherMap API (current weather data endpoint)
    BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

    # Complete URL
    URL = f"{BASE_URL}q=Milan&appid={API_KEY}&units=metric"

    response = requests.get(URL)

    if response.status_code == 200:
        data = response.json() 
        
        main_data = data['main']
        Milan_temperature = main_data['temp']

        # Convert to Kelvin
        return round(get_temperature(city) - 273.15 - Milan_temperature, 2)
    
    else:
        return None