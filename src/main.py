"""Main backend file for the application."""

import uuid
import json
import requests
import time

WEATHER_API_KEY = "38e0e27225dc6cd5efee99d1457f462d"

plants = []


class Plant:
    """Plant class"""
    id: int
    name: str
    description: str
    size: int
    dead: bool = False

    def __init__(self, name, description) -> None:
        self.id = uuid.uuid4()
        self.name = name
        self.description = description
        self.size = 100


def apply_weather(rain: bool):
    """Apply weather to all alive plants"""
    for plant in plants:
        if not plant.dead:
            if rain:
                plant.size += 1
            else:
                plant.size -= 1


def check_dead():
    """Check if plants are dead"""
    for plant in plants:
        if plant.size <= 0:
            plant.dead = True


def get_weather():
    """Get weather from OpenWeatherMap API"""
    # API Call: https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
    # Location of Biel: 47.138466 / 7.247041

    lat = 47.138466
    lon = 7.247041
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}"
    response = requests.get(api_url, timeout=5)
    json_data = json.loads(response.text)
    return json_data


def main():
    """Main function"""
    # Add dummy plant
    plants.append(Plant("Dummy", "Dummy plant"))

    # Mainloop
    while True:
        weather_data = get_weather()
        weather = weather_data["weather"][0]["main"]
        rain = weather == "Rain"
        apply_weather(rain)
        time.sleep(10)

        # Print plants
        for plant in plants:
            print(f"Plant {plant.name} is {'dead' if plant.dead else 'alive'} and has a size of {plant.size}.")


main()