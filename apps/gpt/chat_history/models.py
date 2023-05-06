"""Models for chat history."""
from pydantic import BaseModel

import datetime as dt


class Message(BaseModel):
    """
    A Message is both the user input and the agent response.

    Attributes:
        datetime: The datetime of the message.
        inbound_phone: The inbound phone number.
        user_input: The user input.
        agent_response: The agent response.
    """
    datetime: dt.datetime
    inbound_phone: str
    user_input: str
    agent_response: str

    def to_dict(self) -> dict:
        """Return the message as a dictionary."""
        return {
            "datetime": self.datetime.isoformat(),
            "inbound_phone": self.inbound_phone,
            "user_input": self.user_input,
            "agent_response": self.agent_response
        }
