
"""
Read config.yaml.
"""
import os
import yaml

from config import models


config_path = os.path.join(
    (current_dir := os.path.realpath(os.path.dirname(__file__))),
    "..",  # parent dir since module is in a subdirectory
    "config.yaml"
)

if not os.path.exists(config_path):
    raise FileNotFoundError("config.yaml file not found.")

with open(config_path, "r", encoding="utf-8") as f:
    RAW_CONFIG = yaml.safe_load(f)

# Validate the keys and expose KEYS
CONFIG = models.Keys(**RAW_CONFIG)
