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


class ConfigurationError(Exception):
    """Raise this error if an invalid configuration value is provided."""
    def __init__(self, value, config_path: str = ""):
        message = ""
        if config_path:
            message += f"An invalid configuration was provided for {config_path}. "

        message += f"You provided {value}, which is invalid."
        super().__init__(message)


def read_bool_option(option: str) -> bool:
    """
    Read a boolean preference, ex. true/yes/no, and turn it into a boolean for 
    a config class. Meant to read items from a configuration file that only reads
    text string value.
    """
    if option.lower() in {"true, yes, on"}:
        return True
    elif option.lower() in {"false, no, off"}:
        return False
    else:
        raise ConfigurationError(option)


class General:
    SANDBOX_MODE: bool = read_bool_option(config["General"]["sandbox_mode"])
    THREADED_INBOUND: bool = read_bool_option(config["General"]["threaded_inbound"])


class Weather:
    DEFAULT_CITY: str = config["Weather"]["default_city"]


class Groceries:
    THREADED_INBOUND: bool = read_bool_option(config["Groceries"]["translation"])
    FULL_DT_FORMAT: str = "%Y-%m-%d %H-%M-%S"


class Cocktails:
    RESULT_LIMIT: int = int(config["Cocktails"]["result_limit"])
