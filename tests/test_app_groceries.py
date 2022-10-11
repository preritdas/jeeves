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


def test_help():
    res = app_groceries.handler(
        content = "",
        options = {"help": "yes"}
    )

    assert "setup" in res and "grocery list" in res
