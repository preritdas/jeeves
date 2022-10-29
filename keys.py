"""
Read keys.ini and parse.
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
