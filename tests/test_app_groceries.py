import random

import app_groceries


def test_handler():
    ITEMS = ["Apples", "Bananas", "Blueberries", "snacks", "pears", "limes", "lamb"]
    test_items = random.sample(ITEMS, 2)  # get a few random items for testing

    res = app_groceries.handler(
        content = "\n".join(test_items),
        options = {"setup": "whole foods", "inbound_phone": "12223334455"}
    )

    assert "List ID" in res
    assert "Apples" in res

    # Test adding items with last feature
    res = app_groceries.handler(
        content = "Chicken",
        options = {"inbound_phone": "12223334455", "add": "last"}
    )

    assert "List ID" in res
    assert all(item in res for item in test_items)
    assert "Chicken" in res


def test_help():
    res = app_groceries.handler(
        content = "",
        options = {"help": "yes"}
    )

    assert "setup" in res and "grocery list" in res
