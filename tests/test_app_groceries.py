import random

import app_groceries
from app_groceries import grocery_utils

# Fixtures
from . import default_options


def test_handler():
    ITEMS = ["Apples", "Bananas", "Blueberries", "snacks", "pears", "limes", "lamb"]
    test_items = random.sample(ITEMS, 2)  # get a few random items for testing

    res = app_groceries.handler(
        content = "\n".join(test_items),
        options = {"setup": "whole foods", "inbound_phone": "12223334455"}
    )

    assert "List ID" in res
    assert all(item in res for item in test_items)

    # Test adding items with last feature
    res = app_groceries.handler(
        content = "Chicken",
        options = {"inbound_phone": "12223334455", "add": "last"}
    )

    assert "List ID" in res
    assert "Chicken" in res

    # Test no list found
    assert not "List ID" in app_groceries.handler(
        content = "Apples",
        options = {
            "inbound_phone": "10000000000",
            "add": "last"
        }
    )


def test_no_category(default_options):
    res = app_groceries.handler(
        "random", default_options
    )

    assert "random" in res


def test_translation(mocker, default_options):
    """
    MOCKING DOESN'T WORK HERE.

    For now, just test using the correct translation function, as translation is 
    temporarily disabled due to lxml issues with Python 3.11.
    """
    mocker.patch("config.Groceries.TRANSLATION", True)  # doesn't work
    assert "apples" in app_groceries.handler(
        "apples", default_options
    )


def test_singularization():
    """
    Ensure singularization/pluralization is working in the classifiation mechanism.
    """
    WEIRD_ITEMS = ["blueberries", "lamb", "chicken"]

    res = app_groceries.handler(
        content = "\n".join(WEIRD_ITEMS),
        options = {"inbound_phone": "12223334455"}
    )

    test_res = res.lower()
    assert "fruit" in test_res  # make sure 'blueberries' was properly categorized
    assert "meat" in test_res


def test_paranthesis():
    """Options, ex. chicken (good kind)"""
    res = app_groceries.handler(
        content = "chicken (good kind)",
        options = {
            "inbound_phone": "12223334455"
        }
    )

    assert res
    assert "List ID" in res
    assert "(good kind)" in res


def test_pluralization():
    # Test normal pluralization
    assert grocery_utils.pluralize("tank") == "tanks"

    # Test manual substitution pluralization
    assert grocery_utils.pluralize("pork") == "pork"

    # Test already plural
    assert grocery_utils.pluralize("beans") == "beans"


def test_help():
    res = app_groceries.handler(
        content = "",
        options = {"help": "yes"}
    )

    assert "setup" in res and "grocery list" in res
