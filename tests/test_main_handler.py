"""Testing if texts can be sandboxed with the FastAPI client."""
import inbound
from parsing import InboundMessage


def test_no_permissions(mocker, default_inbound):
    mocker.patch("inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        **default_inbound,
        "phone_number": "192837261629"  # 11 digits as this would never be in the database
    }

    res = inbound.main_handler(InboundMessage(**inbound_payload))

    assert "you don't have permission" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_invalid_app(mocker, default_inbound):
    mocker.patch("inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        **default_inbound,
        "body": "app: askjdcasldjc",
    }

    res = inbound.main_handler(InboundMessage(**inbound_payload))

    assert "app does not exist" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_run_app(mocker, user_git_pytest):
    mocker.patch("inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        "phone_number": user_git_pytest["Phone"],
        "body": "app: apps",
    }

    res = inbound.main_handler(InboundMessage(**inbound_payload))

    assert "available" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_app_error_handling(mocker, user_git_pytest):
    mocker.patch("inbound.texts.CONFIG.General.sandbox_mode", True)
    mocker.patch("inbound.usage.CONFIG.General.sandbox_mode", True)

    inbound_payload = {
        "phone_number": user_git_pytest["Phone"],
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
