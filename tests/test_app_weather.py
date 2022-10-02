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
