"Test the GPT app."
from apps.gpt import handler
from api.voice_inbound import _process_speech
from apps.gpt.make_calls.routes import process_user_speech
from apps.gpt.make_calls.database import Call
from apps.gpt.tool_auth import no_auth_tools, build_tools

from keys import KEYS


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


def test_agency(mocker, default_options, callback_uid):
    """Test the GPT applet handler."""
    mocker.patch("apps.gpt.__init__.uuid.uuid4", return_value=callback_uid)

    res = handler(
        content="Who are you?",
        options=default_options
    )

    assert res
    assert isinstance(res, str)
    assert "Jeeves" in res


def test_processing_speech(mocker, who_are_you_twilio_recording, default_options, callback_uid):
    """
    Test the background process that updates the call with a response when calling 
    Jeeves (inbound).
    """
    mocker.patch("CONFIG.General.sandbox_mode", True)

    response = _process_speech(
        inbound_phone=default_options["inbound_phone"],
        audio_url=who_are_you_twilio_recording,
        call_sid=callback_uid
    )

    assert response
    assert (xml := response.to_xml())
    assert "Play" in xml
    assert "upcdn" in xml


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
    assert "upcdn" in xml
    

def test_serper_wrapper():
    """Test the serper wrapper."""
    serper_tool = no_auth_tools[0]
    
    # Make sure we got the right one
    assert serper_tool.name == "Google Search"

    # Test basic
    res: str = serper_tool.run("united states year of independence")

    assert res
    assert isinstance(res, str)
    assert "1776" in res

    # Test returning links
    link_res: str = serper_tool.run("best car vacuums")

    assert link_res
    assert isinstance(link_res, str)
    assert "https" in link_res


def test_building_tools(default_options, callback_handlers):
    """Test building the tools. Zapier and text requires auth."""
    # Make sure Zapier is in there, use first provided phone 
    if KEYS.ZapierNLA:
        tools = build_tools(
            inbound_phone=list(KEYS.ZapierNLA.keys())[0],
            callback_handlers=callback_handlers
        )
        tool_names = [tool.name for tool in tools]
        tool_descriptions = [tool.description for tool in tools]

        assert any("Zapier" in description for description in tool_descriptions)
    else:
        tools = build_tools(
            inbound_phone=default_options["inbound_phone"],
            callback_handlers=callback_handlers
        )
        tool_names = [tool.name for tool in tools]
        tool_descriptions = [tool.description for tool in tools]

    # General
    assert tools
    assert any("Text Message" in name for name in tool_names)
