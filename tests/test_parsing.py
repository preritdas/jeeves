"""
Parsing is already used and tested indirectly by `test_main_handler`.
This module is for testing long-tail events.
"""
import pytest

from parsing import validate_phone_number


def test_validate_twilio_number():
    assert validate_phone_number("+12223334455") == "12223334455"


def test_validate_already_good():
    assert validate_phone_number("12223334455") == "12223334455"


def test_validate_bad_number():
    with pytest.raises(ValueError):
        validate_phone_number("123")    


def test_validate_bad_type():
    assert validate_phone_number(12223334455) == "12223334455"
