import app_groceries


def test_handler():
    res = app_groceries.handler(
        content = "Apples\nBananas",
        options = {"setup": "whole foods", "inbound_phone": "12223334455"}
    )

    assert "List ID" in res
    assert "Apples" in res


def test_help():
    res = app_groceries.handler(
        content = "",
        options = {"help": "yes"}
    )

    assert "setup" in res and "grocery list" in res
