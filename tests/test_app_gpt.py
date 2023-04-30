"Test the GPT app."
import pytest

from apps.gpt import handler
from api.voice_inbound import _process_speech


def test_handler(default_options):
    """Test the GPT applet handler."""
    # Use vanilla GPT
    default_options["agency"] = "no"

    res = handler(
        content="Give me three short rhyming words.",
        options=default_options
    )

    assert res
    assert isinstance(res, str)


def test_agency(default_options):
    """Test the GPT applet handler."""
    res = handler(
        content="Who are you?",
        options=default_options
    )

    assert res
    assert isinstance(res, str)
    assert "Jeeves" in res


@pytest.mark.xfail(reason="Out of ElevenLabs credits.")
def test_processing_speech(who_are_you_twilio_recording, default_options):
    """
    Test the background process that updates the call with a response when calling 
    Jeeves (inbound).
    """
    response = _process_speech(
        inbound_phone=default_options["inbound_phone"],
        audio_url=who_are_you_twilio_recording
    )

    assert response
    assert (xml := response.to_xml())
    assert "Play" in xml
    assert "uploadio" in xml
