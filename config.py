"""Read config values."""
import os
import configparser


config = configparser.RawConfigParser()
config.read(
    os.path.join(
        (current_dir := os.path.dirname(os.path.realpath(__file__))),
        "config.ini"
    )
)


class Weather:
    default_city = config["Weather"]["default_city"]


class Groceries:
    translation = config["Translation"]["translation"]
