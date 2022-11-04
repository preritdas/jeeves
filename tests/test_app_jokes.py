from apps import app_jokes


def test_handler():
    assert app_jokes.handler("", options={"tags": "nsfw,dark"})


def test_help():
    res = app_jokes.handler("", options={"help": "yes"})
    assert "random joke" in res and "separated categories" in res
