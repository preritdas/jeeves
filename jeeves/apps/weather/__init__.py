"""Weather data."""
from jeeves import utils
from jeeves.config import CONFIG

from jeeves.apps.weather import data
from jeeves.apps.weather.data import kelvin_to_farenheit as farenheit


APP_HELP = "Get weather data."
APP_OPTIONS = {
    "city": f"OPTIONAL, default is {CONFIG.Weather.default_city}",
    "state": "OPTIONAL, U.S. state, city is usually sufficient",
    "country": "OPTIONAL, ISO code, city is usually sufficient"
}


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    """Weather data."""
    city = options.get("city", CONFIG.Weather.default_city)
    state = options.get("state", "")
    country = options.get("country", "")

    weather = data.current_weather(city, state, country)

    if not type(weather) is dict:
        return f"There was an error. {weather}"

    return (
        f"It's currently {farenheit(weather['main']['temp'])} degrees outside. "
        f"Today's high will be {farenheit(weather['main']['temp_max'])} degrees; "
        f"the low will be {farenheit(weather['main']['temp_min'])} degrees. "
        f"The sun will set at {data.sunset_format(weather['sys']['sunset'])}."
    )
