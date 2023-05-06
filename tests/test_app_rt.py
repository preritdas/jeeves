"""Test Rotten Tomatoes app."""
from apps import rt


def test_handler():
    top_gun = rt.handler("top gun", {"inbound_phone": "12223334455"})
    assert "Top Gun" in top_gun

    failed = rt.handler("asdaf;sdkjfa", {"inbound_phone": "12223334455"})
    assert not "\n" in failed  # proper results are line separated. Errors aren't.

    no_content = rt.handler("", {"inbound_phone": "12223334455"})
    assert not "\n" in no_content


def test_help():
    assert "Rotten Tomatoes" in rt.handler("", options={"help": "yes"})
