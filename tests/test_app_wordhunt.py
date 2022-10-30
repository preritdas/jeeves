"""Test the WordHunt app."""
# External
import pytest

# Internal
import random
import string

# Project
import app_wordhunt


@pytest.fixture
def random_board():
    return app_wordhunt.wordhunt.Board.from_letters(
        letters = "".join(random.choices(string.ascii_lowercase, k=16)), 
        width = 4, 
        height = 4
    )


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


def test_string_board(random_board):
    assert "\n" in str(random_board)


def test_value_error(random_board):
    with pytest.raises(ValueError):
        app_wordhunt.wordhunt.Board.from_letters("asd", 4, 4)


def test_print_results_no_limit(random_board):
    possibilities = app_wordhunt.wordhunt.all_possibilities(random_board)
    assert type(app_wordhunt.wordhunt.print_results(possibilities)) is str


def test_help():
    assert "Solve a" in app_wordhunt.handler("", {"help": "yes"})
