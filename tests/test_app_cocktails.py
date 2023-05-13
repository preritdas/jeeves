"""Test the cocktails app."""
import pytest
import requests

from jeeves.applets import cocktails


def test_handler():
    res = cocktails.handler("", {"inbound_phone": "12223334455"})

    # Assert the process succeeded
    assert "behold" in res.lower() and "enjoy" in res.lower()


def test_querying():
    res = cocktails.handler("tequila", {"inbound_phone": "12223334455"})

    # Assert that the right drinks were found
    res_test = res.lower()

    assert "tequila fizz" in res_test
    assert "tequila sour" in res_test


def test_no_query_found():
    res = cocktails.handler("lmfao", {"inbound_phone": "12223334455"})

    # Assert no drink found messages
    assert "find any drink" in res.lower()


def test_no_drink_found_error():
    with pytest.raises(cocktails.errors.DrinkNotFoundError):
        cocktails.data.Drink.from_response(
            requests.get(cocktails.data.ENDPOINT + "search.php?s=lmfao")
        )


def test_not_all_drinks():
    response = requests.get(cocktails.data.ENDPOINT + "search.php?s=tequila")
    drink = cocktails.data.Drink.from_response(response, all_drinks=False)

    assert drink
    assert drink.basic_format
    assert str(drink)


def test_drink_concat():
    assert type(cocktails.data.concat_drinks([])) is str
    assert (
        "behold"
        in cocktails.data.concat_drinks(
            [cocktails.data.Drink("test", {"ing": "1"}, "stuff")]
        ).lower()
    )


def test_help():
    help_text = cocktails.handler("", {"inbound_phone": "12223334455", "help": "yes"})

    assert "cocktail" in help_text.lower() and "drink" in help_text.lower()
