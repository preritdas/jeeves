"""Testing if texts can be sandboxed with the Flask client."""
import inbound


def test_sandbox(mocker):
    mocker.patch("inbound.texts.config.General.SANDBOX_MODE", True)

    content, status_code = inbound.main_handler(
        {
            "msisdn": "14259023246",
            "text": "app: apps"
        }
    )

    assert not content
    assert 200 <= status_code < 300
