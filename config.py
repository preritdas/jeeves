"""
Read config values.

Requires a config.ini file with sections for each class below, in the following
format.

[General]
sandbox_mode = false
threaded_inbound = false

[Weather]
default_city = London

[Groceries]
translation = false
"""
import os
import configparser


config = configparser.RawConfigParser()
config.read(
    os.path.join(
        (current_dir := os.path.dirname(os.path.realpath(__file__))),
        "config.ini"
    )
)


class General:
    SANDBOX_MODE: bool = True if config["General"]["sandbox_mode"].lower() == "true" else False
    THREADED_INBOUND: bool = True if config["General"]["threaded_inbound"].lower() == "true" else False


class Weather:
    DEFAULT_CITY: str = config["Weather"]["default_city"]


class Groceries:
    TRANSLATION: bool = True if config["Groceries"]["translation"].lower().strip() == "true" \
        else False

    FULL_DT_FORMAT: str = "%Y-%m-%d %H-%M-%S"


class Cocktails:
    RESULT_LIMIT: int = int(config["Cocktails"]["result_limit"])
