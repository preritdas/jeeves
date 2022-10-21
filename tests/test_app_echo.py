from re import L
import app_echo


def test_handler():
    res = app_echo.handler(
        content = "This is the message.",
        options = {
            "recipient": "12223334455"
        }
    )

    assert "The following message was sent" in res


def test_no_phone():
    res = app_echo.handler(
        content = "Doesn't matter.",
        options = {}
    )

    assert "You must provide" in res


def test_help():
    res = app_echo.handler(content = "", options = {"help": "yes"})

    assert "Send a message" in res
