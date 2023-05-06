"""Test broad app manager, including app to list apps."""
import apps


def test_handler(default_options):
    assert "The following apps are available" in apps.handler("", default_options)


def test_program_list():
    assert type(apps.PROGRAMS) is dict and all(
        [key for key in apps.PROGRAMS if isinstance(key, str)]
    )


def test_help():
    assert "available apps" in apps.handler(content="", options={"help": "yes"})
