from apps import jokes


def test_handler():
    assert jokes.handler("", options={"tags": "nsfw,dark"})


def test_help():
    res = jokes.handler("", options={"help": "yes"})
    assert "random joke" in res and "separated categories" in res
