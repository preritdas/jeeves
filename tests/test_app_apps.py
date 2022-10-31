import app_apps

# Pytest fixtures
from . import default_options, default_inbound


def test_handler(default_options):
    assert "The following apps are available" in app_apps.handler(
        "", default_options
    )


def test_program_list():
    assert type(app_apps.PROGRAMS) is dict and \
        all([key for key in app_apps.PROGRAMS if isinstance(key, str)])


def test_help():
    assert "available apps" in app_apps.handler(content="", options={"help": "yes"})
