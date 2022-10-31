import random

import app_groceries
from app_groceries import grocery_utils
from app_groceries import grocery_db


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
    test_last_res = app_groceries.handler(
        content = "Chicken",
        options = {"inbound_phone": "12223334455", "add": "last"}
    )

    assert "List ID" in test_last_res
    assert "Chicken" in test_last_res

    # Cleanup original list
    list_id = res[len("List ID") + 2:res.find("\n")]
    grocery_db.delete(list_id)

    # Cleanup last test list
    list_id = test_last_res[len("List ID") + 2:res.find("\n")]
    grocery_db.delete(list_id)

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

    # Cleanup 
    list_id = res[len("List ID") + 2:res.find("\n")]
    grocery_db.delete(list_id)


def test_translation(mocker, default_options):
    """
    MOCKING DOESN'T WORK HERE.

    For now, just test using the correct translation function, as translation is 
    temporarily disabled due to lxml issues with Python 3.11.
    """
    mocker.patch("app_groceries.classification.config.Groceries.TRANSLATION", True)  # doesn't work
    res = app_groceries.handler(
        "apples", default_options
    )

    assert "apples" in res

    # Cleanup
    list_id = res[len("List ID") + 2:res.find("\n")]
    grocery_db.delete(list_id)


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

    # Cleanup
    list_id = res[len("List ID") + 2:res.find("\n")]
    grocery_db.delete(list_id)


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

    # Cleanup
    list_id = res[len("List ID") + 2:res.find("\n")]
    grocery_db.delete(list_id)


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
