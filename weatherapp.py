import requests
import json
import os

API_KEY = "" # haal je eigen key!
BASE_URL = "https://api.weatherapi.com/v1/forecast.json"
CACHE_FILE = "weather_cache.json"

# alle gevraagde inputs
location = input("Van welke plaats wilt u het weer weten?: ")
unit = input("Kies temperatuureenheid (C/F): ").upper()

params = {'key': API_KEY, 'q': location, 'days': 3}  # voorspelt voor de aankomende 3 dagen

weather_icons = {
    "Sunny": "☀️",
    "Partly cloudy": "⛅",
    "Cloudy": "☁️",
    "Rainy": "🌧️",
    "Snowy": "❄️",
}

# kijkt of er al een gecachde file is
if os.path.isfile(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        cache_data = json.load(f)
else:
    cache_data = {}


if location in cache_data:
    data = cache_data[location]
else:
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        # slaat de data in de cache op en checkt of er een error is
        cache_data[location] = data
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)
    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        exit()
    except json.JSONDecodeError as e:
        print("JSON Decode Error:", str(e))
        exit()
    except Exception as e:
        print("Error:", str(e))
        exit()

if 'error' in data:
    print("Error:", data['error']['message'])
else:
    forecast_days = data['forecast']['forecastday']
    for day in forecast_days:
        date = day['date']
        weather = day['day']['condition']['text']
        temperature_c = day['day']['avgtemp_c']
        humidity = day['day']['avghumidity']
        wind_speed_kph = day['day']['maxwind_kph']

        # alternatieve methode om fahrenheit te berekenen
        if unit == 'F':
            temperature = (temperature_c * 9/5) + 32
            wind_speed = round(wind_speed_kph * 0.62137119223733, 2)  # Conversion from km/h to mph
            unit_label = "°F"
            unit_label2 = "mph"
        else:
            temperature = temperature_c
            wind_speed = wind_speed_kph
            unit_label = "°C"
            unit_label2 = "km/h"

        icon = weather_icons.get(weather, "❓")

        print("\nDate:", date)
        print("Weather:", icon, weather)
        print("Temperature:", temperature, unit_label)
        print("Humidity:", humidity, "%")
        print("Wind Speed:", wind_speed, unit_label2)