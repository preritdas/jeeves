"""
Test the invite app. Make sure to pass "preview" to all the handler options 
(except help) to prevent actual text messages from being sent.
"""
import app_invite


def test_handler():
    res = app_invite.handler(
        content = "12223334455",
        options = {
            "preview": "yes"
        }
    )

    assert "Preview of message" in res
    assert "app name statement" in res


def test_no_recipient():
    res = app_invite.handler(
        content = "",
        options = {"preview": "yes"}
    )

    assert not "Successfully" in res


def test_invalid_phone():
    res = app_invite.handler(
        content = "97asdc6d99",
        options = {"preview": "yes"}
    )

    assert "invalid" in res.lower()


def test_help():
    res = app_invite.handler(
        content = "",
        options = {
            "help": "yes"
        }
    )

    assert "doesn't text" in res
