"Test the GPT app."
import pytest

from apps.gpt import handler
from api.voice_inbound import _process_speech
from apps.gpt.make_calls.routes import process_user_speech
from apps.gpt.make_calls.database import Call


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


@pytest.mark.xfail(reason="Out of ElevenLabs credits.")
def test_processing_speech_outbound(outbound_call_key):
    """Test generating the next voice response when outbound calling."""
    call = Call.from_call_id(call_id=outbound_call_key)
    voice_response = process_user_speech(
        call_id=call.key,
        user_speech="Hi there, how can I help you today?"
    )

    assert voice_response
    assert (xml := voice_response.to_xml())
    assert "Play" in xml
    assert "uploadio" in xml
    