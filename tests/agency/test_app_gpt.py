"Test the GPT app."
from jeeves.applets.gpt import handler
from api.voice_inbound import _process_speech
from jeeves.agency.make_calls.routes import process_user_speech
from jeeves.agency.make_calls.database import Call
from jeeves.agency.tool_auth import no_auth_tools, build_tools
from jeeves.agency.logs_callback import extract_log_items

from jeeves.keys import KEYS
from jeeves.permissions.database import permissions_db


def test_handler(default_options):
    """Test the GPT applet handler."""
    # Use vanilla GPT
    default_options["agency"] = "no"

    res = handler(content="Give me three short rhyming words.", options=default_options)

    assert res
    assert isinstance(res, str)


def test_agency(mocker, callback_uid, default_options, temporary_user):
    """Test the GPT applet handler."""
    mocker.patch("jeeves.agency.uuid.uuid4", return_value=callback_uid)

    # Don't add chat logs
    mocker.patch(
        "jeeves.agency.chat_history.database.ChatHistory.add_message", return_value=None
    )

    res = handler(content="Who are you?", options=default_options)

    assert res
    assert isinstance(res, str)
    assert "Jeeves" in res


def test_processing_speech(
    mocker, who_are_you_twilio_recording, default_options, callback_uid, temporary_user
):
    """
    Test the background process that updates the call with a response when calling
    Jeeves (inbound).
    """
    mocker.patch("api.voice_inbound.texts.CONFIG.General.sandbox_mode", True)

    # Don't add chat logs
    mocker.patch(
        "jeeves.agency.chat_history.database.ChatHistory.add_message", return_value=None
    )

    response = _process_speech(
        inbound_phone=default_options["inbound_phone"],
        audio_url=who_are_you_twilio_recording,
        call_sid=callback_uid
    )

    assert response
    assert (xml := response.to_xml())
    assert "Play" in xml
    assert "upcdn" in xml


def test_processing_speech_outbound(outbound_call_key, mocker):
    """Test generating the next voice response when outbound calling."""
    # Don't add chat logs
    mocker.patch(
        "jeeves.agency.chat_history.database.ChatHistory.add_message", return_value=None
    )

    call = Call.from_call_id(call_id=outbound_call_key)
    voice_response = process_user_speech(
        call_id=call.key, user_speech="Hi there, how can I help you today?"
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

    # Test returning links
    link_res: str = serper_tool.run("best car vacuums")

    assert link_res
    assert isinstance(link_res, str)
    assert "https" in link_res


def test_building_tools(default_options, callback_handlers):
    """Test building the tools. Zapier and text requires auth."""
    # Find a temporary Zapier key
    users_with_zapier = permissions_db.fetch(
        {
            "ZapierKey?contains": "sk"
        }
    ).items

    # Make sure Zapier is in there, use first provided phone
    if users_with_zapier:
        tools = build_tools(
            inbound_phone=users_with_zapier[0]["Phone"],
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


def test_log_formatting():
    log = "Thought: Using a thing\nAction: Tool Name\nAction Input: this is an input"
    fields = ["Thought", "Action", "Action Input"]
    log_items = extract_log_items(log, fields)

    assert log_items
    assert isinstance(log_items, list)
    assert all(isinstance(item, str) for item in log_items)
    assert len(log_items) == len(fields)

    # Check that the log items are in the right order
    assert "Thought" in log_items[0]
    assert "Action" in log_items[1] and "Action Input" not in log_items[1]
    assert "ActionInput" in log_items[2]
