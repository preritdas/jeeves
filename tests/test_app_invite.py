import app_invite


def test_handler():
    res = app_invite.handler(
        content = "",
        options = {
            "recipient": "2223334455",
            "preview": "yes"
        }
    )

    assert "Preview of message" in res
    assert "app name statement" in res


def test_help():
    res = app_invite.handler(
        content = "",
        options = {
            "help": "yes"
        }
    )

    assert "doesn't text" in res
