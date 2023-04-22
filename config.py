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
import yaml


with open(
    os.path.join(
        (current_dir := os.path.dirname(os.path.realpath(__file__))),
        "config.yaml"
    ),
    "r",
    encoding="utf-8"
) as config_file:
    CONFIG = yaml.safe_load(config_file)
