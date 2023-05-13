"""Test broad app manager, including app to list apps."""
from jeeves import applets


def test_handler(default_options):
    assert "The following apps are available" in applets.handler("", default_options)


def test_program_list():
    assert type(applets.PROGRAMS) is dict and all(
        [key for key in applets.PROGRAMS if isinstance(key, str)]
    )


def test_help():
    assert "available apps" in applets.handler(content="", options={"help": "yes"})
