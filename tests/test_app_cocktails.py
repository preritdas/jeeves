"""Test the cocktails app."""
import pytest
import requests

import app_cocktails


def test_handler():
    res = app_cocktails.handler("", {"inbound_phone": "12223334455"})

    # Assert the process succeeded
    assert "behold" in res.lower() and "enjoy" in res.lower()


def test_querying():
    res = app_cocktails.handler("tequila", {"inbound_phone": "12223334455"})

    # Assert that the right drinks were found
    res_test = res.lower()

    assert "tequila fizz" in res_test
    assert "tequila sour" in res_test


def test_no_query_found():
    res = app_cocktails.handler("lmfao", {"inbound_phone": "12223334455"})

    # Assert no drink found messages
    assert "find any drink" in res.lower()


def test_no_drink_found_error():
    with pytest.raises(app_cocktails.errors.DrinkNotFoundError):
        app_cocktails.data.Drink.from_response(
            requests.get(
                app_cocktails.data.ENDPOINT + "search.php?s=lmfao"
            )
        )


def test_drink_concat():
    assert type(app_cocktails.data.concat_drinks([])) is str
    assert "behold" in app_cocktails.data.concat_drinks(
        [app_cocktails.data.Drink("test", {"ing": "1"}, "stuff")]
    ).lower()


def test_help():
    help_text = app_cocktails.handler(
        "", 
        {
            "inbound_phone": "12223334455",
            "help": "yes"
        }
    )

    assert "cocktail" in help_text.lower() and "drink" in help_text.lower()
