"""Testing if texts can be sandboxed with the FastAPI client."""
from jeeves import inbound
from jeeves.parsing import InboundMessage


def test_invalid_app(mocker, default_inbound, temporary_user):
    mocker.patch("jeeves.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("jeeves.inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        **default_inbound,
        "body": "app: askjdcasldjc",
    }

    res = inbound.main_handler(InboundMessage(**inbound_payload))

    assert "app does not exist" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_run_app(mocker, temporary_user):
    mocker.patch("jeeves.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("jeeves.inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        "phone_number": temporary_user["Phone"],
        "body": "app: apps",
    }

    res = inbound.main_handler(InboundMessage(**inbound_payload))

    assert "available" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_app_error_handling(mocker, temporary_user):
    mocker.patch("jeeves.inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("jeeves.inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        "phone_number": temporary_user["Phone"],
        "body": (
            "app: wordhunt\n"
            "options: width = notnumber; height = notnumber\n"
            "hagsyausidmsnajs"
        )
    }

    res = inbound.main_handler(InboundMessage(**inbound_payload))

    assert "Unfortunately" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300
