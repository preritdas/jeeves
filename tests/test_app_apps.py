import app_apps


def test_handler():
    assert "The following apps are available" in app_apps.handler(
        "", {"inbound_phone": "12223334455"}
    )


def test_program_list():
    assert type(app_apps.PROGRAMS) is dict and \
        all([key for key in app_apps.PROGRAMS if isinstance(key, str)])


def test_help():
    assert "available apps" in app_apps.handler(content="", options={"help": "yes"})
