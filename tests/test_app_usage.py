"""Test app that reports usage metrics."""
from jeeves.apps import usage


def test_handler():
    res = usage.handler(content="", options={})

    assert "was pinged" in res


def test_help():
    res = usage.handler("", {"help": "yes"})
    assert "usage report" in res
