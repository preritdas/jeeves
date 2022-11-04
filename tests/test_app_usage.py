from apps import app_usage


def test_handler():
    res = app_usage.handler(
        content = "",
        options = {}
    )

    assert "was pinged" in res


def test_help():
    res = app_usage.handler("", {"help": "yes"})
    assert "usage report" in res
