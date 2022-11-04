"""Test Rotten Tomatoes app."""
from apps import app_rt


def test_handler():
    top_gun = app_rt.handler("top gun", {"inbound_phone": "12223334455"})
    assert "Top Gun" in top_gun

    failed = app_rt.handler("asdaf;sdkjfa", {"inbound_phone": "12223334455"})
    assert not "\n" in failed  # proper results are line separated. Errors aren't.

    no_content = app_rt.handler("", {"inbound_phone": "12223334455"})
    assert not "\n" in no_content


def test_help():
    assert "Rotten Tomatoes" in app_rt.handler("", options = {"help": "yes"})
