"""Test the WordHunt app."""
import pytest

import app_wordhunt


# @pytest.mark.skip(reason="Inbound SMS Vonage timeout error, app currently disabled.")
def test_handler():
    res = app_wordhunt.handler(
        content = "nahzuxtskdyxpaus",
        options = {}
    )

    assert "thanx" in res


def test_no_content():
    res = app_wordhunt.handler(
        content = "",
        options = {}
    )

    assert "You must provide" in res


def test_bad_dimensions():
    res = app_wordhunt.handler(
        content = "a", 
        options = {}
    )

    assert "The board is" in res


def test_help():
    assert "Solve a" in app_wordhunt.handler("", {"help": "yes"})
