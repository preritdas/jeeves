"""
Read keys.yaml.
"""
import os
import yaml


keys_path = os.path.join(
    (current_dir := os.path.realpath(os.path.dirname(__file__))),
    "keys.yaml"
)

with open(keys_path, "r") as f:
    KEYS = yaml.safe_load(f)
