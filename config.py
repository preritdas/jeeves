"""
Read config values.

Requires a config.ini file with sections for each class below, in the following
format.


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


class Weather:
    default_city = config["Weather"]["default_city"]


class Groceries:
    translation = True if config["Groceries"]["translation"].lower().strip() == "true" \
        else False
