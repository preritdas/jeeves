"""Testing if texts can be sandboxed with the Flask client."""
import inbound


def test_success(mocker, default_inbound):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)
    mocker.patch("inbound.usage.config.General.SANDBOX_MODE", True)

    res = inbound.main_handler(
        {
            **default_inbound,
        }
    )

    assert res["response"]
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
