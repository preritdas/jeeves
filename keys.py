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


class Twilio:
    """Sending text messages."""
    _twilio_keys = keys["Twilio"]

    ACCOUNT_SID = _twilio_keys["account_sid"]
    AUTH_TOKEN = _twilio_keys["auth_token"]
    SENDER = _twilio_keys["sender"]


class Deta:
    PROJECT_KEY = keys["Deta"]["project_key"]


class HumorAPI:
    API_KEY = keys["Humor API"]["api_key"]


class OpenWeatherMap:
    API_KEY = keys["OpenWeatherMap"]["api_key"]


class OpenAI:
    API_KEY = environment_or_internal("OPENAI_API_KEY", "OpenAI")


class GoogleSerper:
    API_KEY = environment_or_internal("SERPER_API_KEY", "Google Serper")
