import requests

import keys


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


def handler(content: str, options: dict) -> str:
    return random_joke(options.get("tags", ""))
