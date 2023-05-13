"""Test the echo app."""
from jeeves.applets import echo


def test_handler(mocker):
    # Ensure the text isn't actually sent, using sandbox mode.
    mocker.patch("jeeves.applets.echo.texts.CONFIG.General.sandbox_mode", True)

    res = echo.handler(
        content="This is the message.", options={"recipient": "12223334455"}
    )

    assert "The following message was sent" in res


def test_no_phone():
    res = echo.handler(content="Doesn't matter.", options={})

    assert "You must provide" in res


def test_help():
    res = echo.handler(content="", options={"help": "yes"})

    assert "Send a message" in res
