"""Test Rotten Tomatoes app."""
from jeeves.applets import rt


def test_handler():
    top_gun = rt.handler("top gun", {"inbound_phone": "12223334455"})
    assert "Top Gun" in top_gun

    no_content = rt.handler("", {"inbound_phone": "12223334455"})
    assert not "\n" in no_content


def test_help():
    assert "Rotten Tomatoes" in rt.handler("", options={"help": "yes"})
