"""Get data from the OpenWeatherMap API."""
# External
import requests

# Local
import datetime as dt

# Project
import keys


WEATHER_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
GEOCODING_ENDPOINT = "http://api.openweathermap.org/geo/1.0/direct"


def kelvin_to_farenheit(kelvin: float):
    """Conversion."""
    return round(kelvin * 1.8 - 459.67)


def sunset_format(unix: float):
    time = dt.datetime.fromtimestamp(unix)
    formatted = time.strftime("%H:%M")
    hour, minute = formatted.split(":")
    hour = int(hour) - 12
    return f"{hour}:{minute} pm"


def current_weather(
    city: str,
    state: str = "", 
    country: str = ""
) -> dict | str:
    """
    Current weather. A successful response is JSON. A string return value
    indicates an error to be sent back to the user, where the string content is 
    the error message.
    """
    if state and len(state) != 2:
        return "State must be a two digit code."
    if country and len(country) != 2:
        return "Country must be a two digit code."

    response = requests.get(
        WEATHER_ENDPOINT, 
        {
            "q": ",".join([ele for ele in [city.lower(), state.lower(), country.lower()] if ele]), 
            "appid": keys.OpenWeatherMap.api_key
        }
    )

    response: dict = response.json()

    if "message" in response and response["message"] == "city not found":
        return f"The city '{city}' was not found."
    
    return response
