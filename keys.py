"""
Read keys.yaml.
"""
import os
import yaml


keys_path = os.path.join(
    (current_dir := os.path.realpath(os.path.dirname(__file__))),
    "keys.yaml"
)

if not os.path.exists(keys_path):
    raise FileNotFoundError("keys.yaml file not found.")

with open(keys_path, "r") as f:
    KEYS = yaml.safe_load(f)
