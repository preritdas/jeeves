import app_wordhunt


def test_handler():
    res = app_wordhunt.handler(
        content = "nahzuxtskdyxpaus",
        options = {}
    )

    assert "thanx" in res


def test_help():
    assert "Solve a" in app_wordhunt.handler("", {"help": "yes"})
