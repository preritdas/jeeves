"""Weather data."""
import config

from . import data
from .data import kelvin_to_farenheit as farenheit


def handler(content: str, options: dict) -> str:
    """Weather data."""
    if options.get("help", None):
        return "Get weather data.\n\n" \
            "Available options: \n" \
            f"- city: OPTIONAL, default is {config.Weather.default_city}" \
            "- state: OPTIONAL, U.S. state, city is usually sufficient" \
            "- country: OPTIONAL, ISO code, city is usually sufficient"


    city = options.get("city", config.Weather.default_city)
    state = options.get("state", "")
    country = options.get("country", "")

    weather = data.current_weather(city, state, country)

    return f"It's currently {farenheit(weather['main']['temp'])} degrees outside. " \
        f"Today's high will be {farenheit(weather['main']['temp_max'])} degrees; " \
        f"the low will be {farenheit(weather['main']['temp_min'])} degrees. " \
        f"The sun will set at {data.sunset_format(weather['sys']['sunset'])}."
