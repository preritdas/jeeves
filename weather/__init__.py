"""Weather data."""
import config

from . import data
from .data import kelvin_to_farenheit as farenheit


def handler(content: str, options: dict) -> str:
    city = options.get("city", config.Weather.default_city)
    state = options.get("state", "")
    country = options.get("country", "")

    weather = data.current_weather(city, state, country)

    return f"It's currently {farenheit(weather['main']['temp'])} degrees outside. " \
        f"Today's high will be {farenheit(weather['main']['temp_max'])}; the low " \
        f"will be {farenheit(weather['main']['temp_min'])} degrees. " \
        f"The sun will set at {data.sunset_format(weather['sys']['sunset'])}."
