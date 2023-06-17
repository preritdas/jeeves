"""Test the Jokes app."""
import pytest

from jeeves.applets import jokes


@pytest.mark.skip
def test_handler():
    assert jokes.handler("", options={"tags": "nsfw,dark"})


def test_help():
    res = jokes.handler("", options={"help": "yes"})
    assert "random joke" in res and "separated categories" in res
