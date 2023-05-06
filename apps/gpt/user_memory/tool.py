"""
Long term memory tool. Jeeves decides when to store items, 
then uses the tool to retrieve items to get more information.
"""
from deta import Deta

import datetime as dt

from keys import KEYS
from parsing import validate_phone_number
from apps.gpt.user_memory.models import Entry


memory_db = Deta(KEYS.Deta.project_key).Base("user_memory")


class UserMemory:
    def __init__(self, user_phone: str, entries: list[Entry]):
        self.entries = entries
        self.user_phone = validate_phone_number(user_phone)

    @classmethod
    def from_user_phone(cls, user_phone: str) -> None:
        """Get all entries from a user."""
        entries = memory_db.fetch({"user_phone": validate_phone_number(user_phone)}).items
        return cls(user_phone=user_phone, entries=[Entry(**entry) for entry in entries])

    def add_entry(self, content: str) -> None:
        """Add an entry to the user's memory."""
        entry = Entry(
            datetime=dt.datetime.now(),
            user_phone=self.user_phone,
            content=content
        )

        memory_db.put(entry.to_dict())
        return

    def answer_question(self, question: str) -> str:
        """Answer a question from the user's memory."""
        raise NotImplementedError
