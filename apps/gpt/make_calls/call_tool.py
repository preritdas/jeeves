"""The calling tool used by agent."""
from langchain.agents.tools import BaseTool

import json
from urllib.parse import urlencode
from typing import Any, Coroutine

from keys import KEYS
from texts import twilio_client, BASE_URL
from . import database as db
from . import prompts


class CallTool(BaseTool):
    name: str = "Make a Call"
    description: str = (
        "Make a call to a recipient and complete a goal. Input must be a JSON string "
        "with the keys \"recipient_phone\" and \"goal\". The recipient phone number "
        "must be a 10-digit phone number preceded by "
        "country code, ex. \"12223334455\". Do not make up phone numbers - either "
        "use a phone number explicitly provided by the user, or use a phone number from a "
        "tool that provides it for you. Otherwise, do not use this tool."
    )

    def _run(self, query: str) -> str:
        """Make a call."""
        try:
            input_parsed = json.loads(query)
        except Exception as e:
            return f"Error parsing input: {str(e)}"

        if not "recipient_phone" in input_parsed:
            return "Input must have a \"recipient_phone\" key."
        
        if not "goal" in input_parsed:
            return "Input must have a \"goal\" key."

        recipient = str(input_parsed["recipient_phone"])
        goal = str(input_parsed["goal"])

        params = {
            "goal": goal,
            "greeting_id": db.encode_greeting(prompts.generate_intro_message(goal))
        }

        outbound_call = twilio_client.calls.create(
            recipient,
            KEYS["Twilio"]["sender"],
            url=f"{BASE_URL}/voice/outbound/handler?{urlencode(params)}"
        )

        # Wait for call to complete
        while outbound_call.update().status != "completed":
            pass

        return "Call completed."

    def _arun(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, str]:
        raise NotImplementedError()
