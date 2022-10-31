"""Testing if texts can be sandboxed with the Flask client."""
import inbound


def test_no_permissions(mocker, default_inbound):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            **default_inbound,
        }
    )

    assert "you don't have permission" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_message_concat(mocker, default_inbound):
    """If the message is too long."""
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            **default_inbound,
            "text": "test message that is too long and is split by the carrier",
            "concat": "true",
            "concat-part": "1"
        }
    )

    assert "Your message was too long" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_invalid_inbound(mocker, default_inbound):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            **default_inbound,
            "text": "hello",
        }
    )

    assert "invalid" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_invalid_app(mocker, default_inbound):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            **default_inbound,
            "text": "app: askjdcasldjc",
        }
    )

    assert "app does not exist" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_run_app(mocker, user_git_pytest):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            "msisdn": user_git_pytest["Phone"],
            "text": "app: apps",
        }
    )

    assert "available" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300


def test_app_error_handling(mocker, user_git_pytest):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            "msisdn": user_git_pytest["Phone"],
            "text": "app: wordhunt\n" \
                "options: width = notnumber; height = notnumber\n" \
                "hagsyausidmsnajs"
        }
    )

    assert "Unfortunately" in res["response"]
    assert not res["http"][0]
    assert 200 <= res["http"][1] < 300
