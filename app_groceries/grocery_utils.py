"""
Utils.
"""
import mypytoolkit as kit

import json
import os

import nltk; nltk.download(['omw-1.4', 'wordnet', 'wordnet_ic', 'sentiwordnet'], quiet=True, raise_on_error=True)
from pattern import en as pattern


# ---- CONSTANTS ---- 

current_dir = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(current_dir, "pluralization_replacements.json")) as f:
    PLURAL_REPLACEMENTS: dict[str, str] = json.load(f)
    SINGULAR_REPLACEMENTS = {val: key for key, val in PLURAL_REPLACEMENTS.items()}

with open(os.path.join(current_dir, "mapping.json")) as f:
    RAW_MAPPING: dict[str, list[str]] = json.load(f)

with open(os.path.join(current_dir, "setups.json")) as f:
    SETUPS: dict[str, list[str]] = json.load(f)


def MAPPING(setup: str = None) -> dict[str, list[str]]:
    """Return a mapping for a given setup. Default is the raw mapping."""
    if setup is None:
        return RAW_MAPPING

    return kit.reorder_dict(SETUPS[setup.title()], RAW_MAPPING)


def pluralize(word: str) -> str:
    """
    Use the pattern library to smartly and correctly pluralize the word.
    """
    assert isinstance(word, str)
    return pattern.pluralize(word, custom=PLURAL_REPLACEMENTS)


def singularize(word: str) -> str:
    """
    Use the pattern library to smartly and correctly pluralize the word.
    """
    assert isinstance(word, str)
    return pattern.singularize(word, SINGULAR_REPLACEMENTS)
 