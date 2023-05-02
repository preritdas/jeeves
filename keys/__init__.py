"""
Read keys.yaml.
"""
import os
import yaml

from keys import models


keys_path = os.path.join(
    (current_dir := os.path.realpath(os.path.dirname(__file__))),
    "..",  # parent dir since module is in a subdirectory
    "keys.yaml"
)

if not os.path.exists(keys_path):
    raise FileNotFoundError("keys.yaml file not found.")

with open(keys_path, "r", encoding="utf-8") as f:
    RAW_KEYS = yaml.safe_load(f)


# Validate the keys and expose KEYS
KEYS = models.Keys(**RAW_KEYS)
