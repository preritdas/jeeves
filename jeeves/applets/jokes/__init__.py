"""Use HumorAPI to find jokes."""
import requests

from functools import wraps

from jeeves import utils
from jeeves.keys import KEYS


APP_HELP = "Get a random joke."
APP_OPTIONS = {"tags": "comma separated categories, ex. nsft,dark"}


def retry_joke(function):
    """Decorator to retry joke getter."""
    @wraps(function)
    def wrapper(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            # Try one more time or raise
            return function(*args, **kwargs)

    return wrapper


@retry_joke
def random_joke(tags: str):
    endpoint = "https://api.humorapi.com/jokes/random"
    response = requests.get(
        endpoint, params={"include-tags": tags, "api-key": KEYS.HumorAPI.api_key}
    )

    return response.json()["joke"]


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    return random_joke(options.get("tags", ""))
