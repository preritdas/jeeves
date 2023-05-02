"""Interact with a chats Deta Base to facilitate chat history."""
import deta

import datetime as dt

from keys import KEYS
from apps.gpt.chat_history.models import Message
from apps.gpt.chat_history.filter import BaseFilterer


# Initialize the chats Deta Base
chats_base = deta.Deta(KEYS.Deta.project_key).Base("chats")


class ChatHistory:
    """
    A chat history object to interact with the database.
    
    `dt.datetime` is stored in the database in string format, isoformat.
    Serialize datetimes using `dt.datetime.isoformat()` into the database,
    and deserialize using `dt.datetime.fromisoformat()`.
    """
    def __init__(self, messages: list[Message]) -> None:
        """Initialize the chat history."""
        self.messages = messages

    def filter_messages(self, filterer: BaseFilterer) -> list[Message]:
        """
        Filter messages by datetime. Returns a list of Messages.
        """
        return filterer.filter_messages(self.messages)

    @classmethod
    def from_inbound_phone(cls, inbound_phone: str) -> "ChatHistory":
        """
        Retrieve chat history from the database.
        """
        user_messages = chats_base.fetch({"inbound_phone": inbound_phone}).items

        # Parse the messages into a list of Message objects
        messages = [
            Message(
                datetime=dt.datetime.fromisoformat(message["datetime"]),
                user_input=message["user_input"],
                agent_response=message["agent_response"],
                inbound_phone=message["inbound_phone"]
            )
            for message in user_messages
        ]

        return cls(messages=messages)

    def add_message(self, message: Message) -> str:
        """
        Add a message to the database. 
        Returns a dictionary of the full database entry.
        """
        return chats_base.put(message.to_dict())
