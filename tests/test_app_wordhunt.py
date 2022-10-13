"""Test the WordHunt app."""
import pytest

import app_wordhunt


@pytest.mark.skip(reason="Inbound SMS Vonage timeout error, app currently disabled.")
def test_handler():
    res = app_wordhunt.handler(
        content = "nahzuxtskdyxpaus",
        options = {}
    )

    assert "thanx" in res


def test_help():
    assert "Solve a" in app_wordhunt.handler("", {"help": "yes"})
