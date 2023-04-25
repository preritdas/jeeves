"""The calling tool used by agent."""
from langchain.agents.tools import BaseTool

from typing import Any, Coroutine


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
        pass

    def _arun(self, *args: Any, **kwargs: Any) -> Coroutine[Any, Any, str]:
        raise NotImplementedError()
