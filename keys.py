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

    api_key = _nexmo_keys["api_key"]
    api_secret = _nexmo_keys["api_secret"]
    sender = _nexmo_keys["sender"]
    mynumber = _nexmo_keys["receiver"]


class Deta:
    project_key = keys["Deta"]["project_key"]
