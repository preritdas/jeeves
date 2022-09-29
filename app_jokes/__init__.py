import requests

import utils
import keys


APP_HELP = "Get a random joke."
APP_OPTIONS = {
    "tags": "comma separated categories, ex. nsft,dark"
}


def random_joke(tags: str):
    endpoint = "https://api.humorapi.com/jokes/random"
    response = requests.get(
        endpoint,
        params = {
            "include-tags": tags,
            "api-key": keys.HumorAPI.api_key
        }
    )

    return response.json()["joke"]


@utils.app_handler(APP_HELP, APP_OPTIONS)
def handler(content: str, options: dict) -> str:
    return random_joke(options.get("tags", ""))
