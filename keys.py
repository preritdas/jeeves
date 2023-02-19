"""
Read keys.ini and parse. Supply keys.ini in the following format.


[Nexmo]
api_key = 
api_secret = 
sender = 
receiver = 


[Deta]
...
"""
import os
import configparser


keys = configparser.RawConfigParser()
keys.read(
    os.path.join(
        (current_dir := os.path.realpath(os.path.dirname(__file__))),
        "keys.ini"
    )
)


def environment_or_internal(env: str, provider: str) -> str:
    """
    Checks for a key in the environment, and if it's not there, looks inside a 
    keys.ini file. Assumes the key in keys.ini is stored as `api_key`. A `KeyError`
    will be raised if the key cannot be found in either environment or keys.ini.

    This method is necessary as opposed to using `os.environ.get` because if a key is
    in the environment and not in keys.ini, we don't want to check keys.ini for a default
    value and raise a `KeyError`.
    """
    try:
        return os.environ[env]
    except KeyError:  # not in the environment, check keys.ini
        return keys[provider]["api_key"]  # raise KeyError if not found


class Nexmo:
    """Sending text messages."""
    _nexmo_keys = keys["Nexmo"]

    API_KEY = _nexmo_keys["api_key"]
    API_SECRET = _nexmo_keys["api_secret"]
    SENDER = _nexmo_keys["sender"]
    MY_NUMBER = _nexmo_keys["receiver"]


class Deta:
    PROJECT_KEY = keys["Deta"]["project_key"]


class HumorAPI:
    API_KEY = keys["Humor API"]["api_key"]


class OpenWeatherMap:
    API_KEY = keys["OpenWeatherMap"]["api_key"]


class OpenAI:
    API_KEY = environment_or_internal("OPENAI_API_KEY", "OpenAI")
