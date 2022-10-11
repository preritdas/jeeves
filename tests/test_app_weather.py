import app_weather


def test_handler():
    res = app_weather.handler(
        content = "",
        options = {}
    )

    assert res

    # Test custom city
    res = app_weather.handler(
        content = "",
        options = {"city": "London"}
    )

    assert res


def test_help():
    assert "weather data" in app_weather.handler("", {"help": "yes"})


def test_data_invalid_info():
    """
    Test invalid state and country codes in the app_weather.data.current_weather 
    function.
    """
    res = app_weather.handler("", {"inbound_phone": "12223334455", "state": "lol"})
    assert "State must be" in res

    res = app_weather.handler("", {"inbound_phone": "12223334455", "country": "lol"})
    assert "Country must be" in res


def test_invalid_city():
    CITY = "notacity"

    res = app_weather.handler("", {"inbound_phone": "12223334455", "city": CITY})
    assert "was not found" in res
    assert CITY in res  # make sure the bad input is sent back to user
