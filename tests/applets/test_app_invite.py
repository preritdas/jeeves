"""
Test the invite app. Make sure to pass "preview" to all the handler options 
(except help) to prevent actual text messages from being sent.
"""
import pytest

from twilio.rest import Client  # mock an invalid client
from twilio.base.exceptions import TwilioRestException

from jeeves.applets import invite
from keys import KEYS


def test_handler():
    res = invite.handler(content="12223334455", options={"preview": "yes"})

    assert "Preview of message" in res
    assert "app name statement" in res


def test_no_recipient():
    res = invite.handler(content="", options={"preview": "yes"})

    assert not "Successfully" in res


def test_invalid_phone():
    res = invite.handler(content="97asdc6d99", options={"preview": "yes"})

    assert "invalid" in res.lower()


def test_inviting(mocker, default_options):
    mocker.patch("jeeves.applets.invite.texts.CONFIG.General.sandbox_mode", True)
    res = invite.handler("14259023246", default_options)
    assert "Successfully invited" in res


def test_failed_delivery(mocker, default_options):
    """Mock a bad API key."""
    mocker.patch("jeeves.texts.twilio_client", Client(KEYS.Twilio.account_sid, "invalid"))

    with pytest.raises(TwilioRestException):
        invite.handler("14259023246", default_options)


def test_help():
    res = invite.handler(content="", options={"help": "yes"})

    assert "doesn't text" in res
