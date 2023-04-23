"""Wrapper around texts to work best as an agent."""
from langchain.agents.tools import BaseTool

import json
from typing import Any, Coroutine

import texts


class TextMessageTool(BaseTool):
    """Wrapper around texts to work best as an agent."""
    name: str = "Send Text Message"
    description=(
        "Useful for when you need to send a text message. Input must be a JSON string with "
        "the keys \"content\" and \"recipient\" (10-digit phone number preceded by "
        "country code, ex. \"12223334455\"."
    )

    def _run(self, query: str) -> str:
        """Send a text message."""
        input_parsed = json.loads(query)

        # Validate
        assert "content" in input_parsed, "Input must have a \"content\" key."
        assert isinstance(input_parsed["content"], str), "Content must be a string."
        content = input_parsed["content"]

        assert "recipient" in input_parsed, "Input must have a \"recipient\" key."
        assert len(input_parsed["recipient"]) == 11, \
            "Recipient must be a phone number preceded by country code."
        recipient = str(input_parsed["recipient"])

        try:
            return texts.send_message(content=content, recipient=recipient)
        except Exception as e:
            return f"Error: {str(e)}"

    def _arun(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, str]:
        raise NotImplementedError(f"{type(self).__name__} does not support async.")
