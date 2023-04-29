"""The calling tool used by agent."""
from langchain.agents.tools import BaseTool

import json
import time
from urllib.parse import urlencode
from typing import Any, Coroutine

from keys import KEYS
from texts import twilio_client, BASE_URL
from . import database as db
from . import prompts


def make_call(recipient: str, goal: str, recipient_desc: str) -> str:
    """Makes the call and returns a transcript."""
    call_params: dict[str, str] = {
        "call_id": db.create_call(
            goal=goal,
            greeting=prompts.generate_intro_message(goal, recipient_desc),
            recipient_desc=recipient_desc
        )
    }

    outbound_call = twilio_client.calls.create(
        recipient,
        KEYS["Twilio"]["sender"],
        url=f"{BASE_URL}/voice/outbound/handler?{urlencode(call_params)}",
        record=True
    )

    CALL_END_STATUSES = {"completed", "canceled", "failed", "busy", "no-answer"}

    # Wait for call to complete
    while (status := outbound_call.update().status) not in CALL_END_STATUSES:
        time.sleep(1)

    # Return a transcript
    transcript = db.decode_convo(call_params["call_id"])
    return f"Call status: {status} || BEGIN TRANSCRIPT || {transcript} || END TRANSCRIPT ||"


class CallTool(BaseTool):
    name: str = "Make a Call"
    description: str = (
        "Make a call to a recipient and complete a goal. Input must be a JSON string "
        "with the keys \"recipient_phone\", \"recipient_desc\", and \"goal\". The recipient phone number "
        "must be a 10-digit phone number preceded by "
        "country code, ex. \"12223334455\". Do not make up phone numbers - either "
        "use a phone number explicitly provided by the user, or use a phone number from a "
        "tool that provides it for you. Otherwise, do not use this tool. "
        "\"recipient_desc\" is a short description of who you are calling."
        "The \"goal\" should be comprehensive and specific, providing all information necessary "
        "to facilitate a desirable outcome. For example, if you are asked to make a dinner "
        "reservation, you will need a date, time, and name. If you don't have all that you need, "
        "do not use the tool, respond to me and inform me that you're missing critical information. "
        "The output of this tool is a transcript of the call, "
        "so if you don't see an indication that the goal succeeded in the transcript, report that. "
        "Do not assume the goal succeeded unless you see proof in the transcript. For example, "
        "if your task was to inform John that I'm busy tomorrow, and you don't see the recipient (John)"
        "acknowledging this in the returned transcript, consider the message delivery a failure. "
        "Further, if you don't receive any output from this tool, consider the entire call failed."
    )

    def _run(self, query: str) -> str:
        """Make a call."""
        try:
            input_parsed = json.loads(query)
        except Exception as e:
            return f"Error parsing input: {str(e)}"

        if not "recipient_phone" in input_parsed:
            return "Input must have a \"recipient_phone\" key."

        if not "recipient_desc" in input_parsed:
            return "Input must have a \"recipient_desc\" key."
        
        if not "goal" in input_parsed:
            return "Input must have a \"goal\" key."

        return make_call(
            recipient=str(input_parsed["recipient_phone"]),
            goal=str(input_parsed["goal"]),
            recipient_desc=str(input_parsed["recipient_desc"])
        )

    def _arun(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, str]:
        raise NotImplementedError()
